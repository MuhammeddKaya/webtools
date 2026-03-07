import subprocess
from django.contrib import admin, messages
from django.conf import settings
from django.shortcuts import redirect
from django.urls import path
from django.template.response import TemplateResponse
from .models import DeployLog


@admin.register(DeployLog)
class DeployLogAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'branch', 'status', 'triggered_by', 'created_at']
    list_filter = ['status', 'branch']
    readonly_fields = ['triggered_by', 'status', 'branch', 'commit_before', 'commit_after', 'output', 'created_at']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('deploy-now/', self.admin_site.admin_view(self.deploy_view), name='deploy-now'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_deploy_button'] = True
        return super().changelist_view(request, extra_context=extra_context)

    def deploy_view(self, request):
        if request.method == 'POST' and request.user.is_superuser:
            repo_path = getattr(settings, 'GIT_REPO_PATH', '/app')
            log = DeployLog(triggered_by=request.user, status='running')

            try:
                # Add safe directory exception for git in Docker
                subprocess.run(
                    ['git', 'config', '--global', '--add', 'safe.directory', repo_path],
                    capture_output=True, text=True
                )

                # Get current commit
                result_before = subprocess.run(
                    ['git', 'rev-parse', 'HEAD'],
                    cwd=repo_path, capture_output=True, text=True, timeout=10
                )
                log.commit_before = result_before.stdout.strip()[:40]

                # Get current branch
                result_branch = subprocess.run(
                    ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                    cwd=repo_path, capture_output=True, text=True, timeout=10
                )
                log.branch = result_branch.stdout.strip()

                # Git pull
                result = subprocess.run(
                    ['git', 'pull', 'origin', log.branch],
                    cwd=repo_path, capture_output=True, text=True, timeout=60
                )

                # Get new commit
                result_after = subprocess.run(
                    ['git', 'rev-parse', 'HEAD'],
                    cwd=repo_path, capture_output=True, text=True, timeout=10
                )
                log.commit_after = result_after.stdout.strip()[:40]

                log.output = f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"

                if result.returncode == 0:
                    log.status = 'success'

                    # Run collectstatic
                    cs = subprocess.run(
                        ['python', 'manage.py', 'collectstatic', '--noinput'],
                        cwd=repo_path, capture_output=True, text=True, timeout=60
                    )
                    log.output += f"\n\nCOLLECTSTATIC:\n{cs.stdout}"

                    # Run migrate
                    mg = subprocess.run(
                        ['python', 'manage.py', 'migrate', '--noinput'],
                        cwd=repo_path, capture_output=True, text=True, timeout=60
                    )
                    log.output += f"\n\nMIGRATE:\n{mg.stdout}"

                    messages.success(request, f'Deploy başarılı! {log.commit_before[:7]} → {log.commit_after[:7]}')
                else:
                    log.status = 'error'
                    messages.error(request, f'Deploy hatası: {result.stderr[:200]}')

            except subprocess.TimeoutExpired:
                log.status = 'error'
                log.output = 'Timeout: İşlem zaman aşımına uğradı.'
                messages.error(request, 'Deploy timeout!')
            except Exception as e:
                log.status = 'error'
                log.output = str(e)
                messages.error(request, f'Deploy hatası: {e}')

            log.save()
        else:
            messages.warning(request, 'Sadece superuser deploy yapabilir.')

        return redirect('admin:deploy_deploylog_changelist')
