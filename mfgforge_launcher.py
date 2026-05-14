from __future__ import annotations

import os
import sys
import tempfile
import threading
import time
import webbrowser
from pathlib import Path

from app import create_app

APP_HOST = '127.0.0.1'
APP_PORT = 8765
APP_URL = f'http://{APP_HOST}:{APP_PORT}'


def app_data_dir() -> Path:
    if getattr(sys, 'frozen', False):
        base = os.environ.get('LOCALAPPDATA') or str(Path.home())
        return Path(base) / 'MFGForge'
    return Path(__file__).resolve().parent / 'instance'


def configure_runtime_database(health_check: bool = False) -> None:
    if health_check:
        check_dir = Path(tempfile.mkdtemp(prefix='mfgforge_health_'))
        os.environ['MFGFORGE_DATABASE'] = str(check_dir / 'mfgforge_health.sqlite')
    else:
        data_dir = app_data_dir()
        data_dir.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault('MFGFORGE_DATABASE', str(data_dir / 'mfgforge.sqlite'))
    os.environ.setdefault('MFGFORGE_SECRET_KEY', 'mfgforge-local-desktop-runtime')


def run_health_check() -> int:
    configure_runtime_database(health_check=True)
    app = create_app({'TESTING': True})
    client = app.test_client()
    required_paths = [
        '/',
        '/company-pulse',
        '/ai-policy',
        '/records/customers',
        '/records/material-certificates/new',
        '/records/machine-utilization/new',
        '/records/supplier-performance/new',
        '/records/quote-intakes/new',
    ]
    for path in required_paths:
        response = client.get(path)
        if response.status_code != 200:
            print(f'MFGForge health check failed: {path} returned {response.status_code}')
            return 1
    print('MFGForge launcher health check passed.')
    return 0


def open_browser_later() -> None:
    time.sleep(1.0)
    webbrowser.open(APP_URL)


def run_desktop_server() -> None:
    configure_runtime_database(health_check=False)
    app = create_app()
    threading.Thread(target=open_browser_later, daemon=True).start()
    print(f'MFGForge running at {APP_URL}')
    print('Close this window to stop MFGForge.')
    app.run(host=APP_HOST, port=APP_PORT, debug=False, use_reloader=False)


def main() -> int:
    if '--health-check' in sys.argv:
        return run_health_check()
    run_desktop_server()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
