import hashlib
import hmac
import json
import subprocess

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import DeployLog


@csrf_exempt
@require_POST
def webhook_deploy(request):
    """
    GitHub/GitLab webhook endpoint for auto-deploy.

    Setup:
    1. Go to your GitHub repo -> Settings -> Webhooks -> Add webhook
    2. Payload URL: http://YOUR_SERVER_IP/deploy/webhook/
    3. Content type: application/json
    4. Secret: same as GIT_DEPLOY_TOKEN in your .env
    5. Events: Just the push event

    Or call manually:
    curl -X POST http://YOUR_SERVER_IP/deploy/webhook/ \
         -H "X-Deploy-Token: YOUR_TOKEN"
    """
    token = getattr(settings, 'GIT_DEPLOY_TOKEN', '')

    if not token:
        return JsonResponse({'error': 'Deploy token not configured'}, status=500)

    # Check token - support both GitHub signature and custom header
    github_sig = request.headers.get('X-Hub-Signature-256', '')
    custom_token = request.headers.get('X-Deploy-Token', '')

    if github_sig:
        # GitHub webhook signature verification
        expected = 'sha256=' + hmac.new(
            token.encode(), request.body, hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(github_sig, expected):
            return JsonResponse({'error': 'Invalid signature'}, status=403)
    elif custom_token:
        if custom_token != token:
            return JsonResponse({'error': 'Invalid token'}, status=403)
    else:
        return JsonResponse({'error': 'No auth provided'}, status=401)

    # Execute deploy
    repo_path = getattr(settings, 'GIT_REPO_PATH', '/app')
    log = DeployLog(status='running', branch='main')

    try:
        # Get current commit
        before = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            cwd=repo_path, capture_output=True, text=True, timeout=10
        )
        log.commit_before = before.stdout.strip()[:40]

        # Git pull
        result = subprocess.run(
            ['git', 'pull', 'origin', 'main'],
            cwd=repo_path, capture_output=True, text=True, timeout=60
        )

        # Get new commit
        after = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            cwd=repo_path, capture_output=True, text=True, timeout=10
        )
        log.commit_after = after.stdout.strip()[:40]

        output_parts = [f"PULL:\n{result.stdout}\n{result.stderr}"]

        if result.returncode == 0:
            # collectstatic
            cs = subprocess.run(
                ['python', 'manage.py', 'collectstatic', '--noinput'],
                cwd=repo_path, capture_output=True, text=True, timeout=60
            )
            output_parts.append(f"COLLECTSTATIC:\n{cs.stdout}")

            # migrate
            mg = subprocess.run(
                ['python', 'manage.py', 'migrate', '--noinput'],
                cwd=repo_path, capture_output=True, text=True, timeout=60
            )
            output_parts.append(f"MIGRATE:\n{mg.stdout}")

            log.status = 'success'
        else:
            log.status = 'error'

        log.output = '\n\n'.join(output_parts)
        log.save()

        return JsonResponse({
            'status': log.status,
            'commit_before': log.commit_before,
            'commit_after': log.commit_after,
        })

    except Exception as e:
        log.status = 'error'
        log.output = str(e)
        log.save()
        return JsonResponse({'error': str(e)}, status=500)
