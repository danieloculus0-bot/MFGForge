from __future__ import annotations

import os
from pathlib import Path

from superforge_app import create_superforge_app


def configure_hosted_runtime() -> None:
    """Set safe hosted-runtime defaults without seeding fake data."""
    instance_dir = Path(__file__).resolve().parent / 'instance'
    instance_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault('MFGFORGE_DATABASE', str(instance_dir / 'superforge.sqlite'))
    os.environ.setdefault('MFGFORGE_SECRET_KEY', 'change-this-secret-for-deployment')


configure_hosted_runtime()
app = create_superforge_app()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '8080'))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
