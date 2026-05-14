from __future__ import annotations

import os
from pathlib import Path

from superforge_app import create_superforge_app


def configure_replit_runtime() -> None:
    instance_dir = Path(__file__).resolve().parent / 'instance'
    instance_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault('MFGFORGE_DATABASE', str(instance_dir / 'superforge_replit_demo.sqlite'))
    os.environ.setdefault('MFGFORGE_SECRET_KEY', 'superforge-replit-demo-runtime')


configure_replit_runtime()
app = create_superforge_app()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5000'))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
