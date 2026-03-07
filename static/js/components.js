/* ================================================
   WebTools — Shared Components (Vanilla JS)
   ================================================ */

/**
 * DragDropUpload — Enhanced file upload with drag & drop
 */
class DragDropUpload {
    constructor(dropzoneEl, options = {}) {
        this.el = dropzoneEl;
        this.input = dropzoneEl.querySelector('input[type="file"]');
        this.options = {
            maxSize: options.maxSize || 50 * 1024 * 1024, // 50MB default
            accept: options.accept || null,
            multiple: options.multiple ?? this.input?.multiple ?? false,
            onFilesAdded: options.onFilesAdded || (() => { }),
            onFileRemoved: options.onFileRemoved || (() => { }),
        };
        this.files = [];
        this._init();
    }

    _init() {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(evt => {
            this.el.addEventListener(evt, e => { e.preventDefault(); e.stopPropagation(); });
        });
        this.el.addEventListener('dragenter', () => this.el.classList.add('dragover'));
        this.el.addEventListener('dragover', () => this.el.classList.add('dragover'));
        this.el.addEventListener('dragleave', () => this.el.classList.remove('dragover'));
        this.el.addEventListener('drop', e => {
            this.el.classList.remove('dragover');
            const dt = e.dataTransfer;
            if (dt.files.length) this._handleFiles(dt.files);
        });
        if (this.input) {
            this.input.addEventListener('change', () => {
                if (this.input.files.length) this._handleFiles(this.input.files);
            });
        }
    }

    _handleFiles(fileList) {
        const newFiles = Array.from(fileList).filter(f => {
            if (f.size > this.options.maxSize) {
                Toast.show(`File "${f.name}" is too large (max ${this._formatSize(this.options.maxSize)})`, 'error');
                return false;
            }
            return true;
        });
        if (this.options.multiple) {
            this.files = [...this.files, ...newFiles];
        } else {
            this.files = newFiles.slice(0, 1);
        }
        this.options.onFilesAdded(this.files, newFiles);
    }

    removeFile(index) {
        const removed = this.files.splice(index, 1)[0];
        this.options.onFileRemoved(removed, this.files);
    }

    _formatSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / 1048576).toFixed(1) + ' MB';
    }
}

/**
 * FileListUI — Renders a sortable file list
 */
class FileListUI {
    constructor(containerEl, options = {}) {
        this.el = containerEl;
        this.sortable = options.sortable ?? false;
        this.onReorder = options.onReorder || (() => { });
        this.onRemove = options.onRemove || (() => { });
        this.files = [];
    }

    render(files) {
        this.files = files;
        if (!files.length) { this.el.innerHTML = ''; return; }
        this.el.innerHTML = files.map((f, i) => `
      <li class="wt-file-item" draggable="${this.sortable}" data-index="${i}">
        ${this.sortable ? '<span class="wt-file-item__handle" aria-label="Drag to reorder"><i class="bi bi-grip-vertical"></i></span>' : ''}
        <span class="wt-file-item__icon"><i class="bi ${this._getIcon(f.name)}"></i></span>
        <div class="wt-file-item__info">
          <div class="wt-file-item__name">${this._escapeHtml(f.name)}</div>
          <div class="wt-file-item__size">${this._formatSize(f.size)}</div>
        </div>
        <button type="button" class="wt-file-item__remove" data-index="${i}" aria-label="Remove file">
          <i class="bi bi-x-lg"></i>
        </button>
      </li>
    `).join('');

        // Remove buttons
        this.el.querySelectorAll('.wt-file-item__remove').forEach(btn => {
            btn.addEventListener('click', () => {
                const idx = parseInt(btn.dataset.index);
                this.onRemove(idx);
            });
        });

        // Sortable drag
        if (this.sortable) this._initDragSort();
    }

    _initDragSort() {
        let dragIdx = null;
        this.el.querySelectorAll('.wt-file-item').forEach(item => {
            item.addEventListener('dragstart', e => {
                dragIdx = parseInt(item.dataset.index);
                item.classList.add('dragging');
                e.dataTransfer.effectAllowed = 'move';
            });
            item.addEventListener('dragend', () => {
                item.classList.remove('dragging');
                dragIdx = null;
            });
            item.addEventListener('dragover', e => {
                e.preventDefault();
                e.dataTransfer.dropEffect = 'move';
            });
            item.addEventListener('drop', e => {
                e.preventDefault();
                const dropIdx = parseInt(item.dataset.index);
                if (dragIdx !== null && dragIdx !== dropIdx) {
                    this.onReorder(dragIdx, dropIdx);
                }
            });
        });
    }

    _getIcon(name) {
        const ext = name.split('.').pop().toLowerCase();
        const map = {
            pdf: 'bi-file-earmark-pdf-fill',
            jpg: 'bi-file-earmark-image', jpeg: 'bi-file-earmark-image',
            png: 'bi-file-earmark-image', webp: 'bi-file-earmark-image',
            gif: 'bi-file-earmark-image', bmp: 'bi-file-earmark-image',
            svg: 'bi-file-earmark-image',
            mp3: 'bi-file-earmark-music', wav: 'bi-file-earmark-music',
            ogg: 'bi-file-earmark-music', flac: 'bi-file-earmark-music',
            m4a: 'bi-file-earmark-music',
            pptx: 'bi-file-earmark-slides', ppt: 'bi-file-earmark-slides',
        };
        return map[ext] || 'bi-file-earmark';
    }

    _formatSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / 1048576).toFixed(1) + ' MB';
    }

    _escapeHtml(str) {
        const d = document.createElement('div');
        d.textContent = str;
        return d.innerHTML;
    }
}

/**
 * Toast — Simple notification system
 */
class Toast {
    static container = null;

    static _ensureContainer() {
        if (!Toast.container) {
            Toast.container = document.createElement('div');
            Toast.container.className = 'wt-toast-container';
            document.body.appendChild(Toast.container);
        }
    }

    static show(message, type = 'success', duration = 4000) {
        Toast._ensureContainer();
        const el = document.createElement('div');
        el.className = `wt-toast wt-toast--${type}`;
        el.innerHTML = `<i class="bi ${type === 'success' ? 'bi-check-circle' : 'bi-exclamation-circle'}"></i> ${message}`;
        Toast.container.appendChild(el);
        setTimeout(() => {
            el.style.opacity = '0';
            el.style.transform = 'translateX(100px)';
            el.style.transition = 'all 0.3s ease';
            setTimeout(() => el.remove(), 300);
        }, duration);
    }
}

/**
 * copyToClipboard — Copy text to clipboard with toast feedback
 */
function copyToClipboard(text, successMsg = 'Copied to clipboard!') {
    navigator.clipboard.writeText(text).then(() => {
        Toast.show(successMsg, 'success');
    }).catch(() => {
        // Fallback
        const ta = document.createElement('textarea');
        ta.value = text;
        ta.style.position = 'fixed';
        ta.style.left = '-9999px';
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        Toast.show(successMsg, 'success');
    });
}

/**
 * formatSize — Human readable file size
 */
function formatSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / 1048576).toFixed(1) + ' MB';
}

/**
 * Mobile nav toggle
 */
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.querySelector('.wt-navbar__toggle');
    const nav = document.querySelector('.wt-navbar__nav');
    if (toggle && nav) {
        toggle.addEventListener('click', () => nav.classList.toggle('active'));
    }
});
