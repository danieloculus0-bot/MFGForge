from __future__ import annotations

import os
import tempfile
from pathlib import Path

os.environ['MFGFORGE_DATABASE'] = str(Path(tempfile.mkdtemp(prefix='superforge_replit_verify_')) / 'verify.sqlite')
os.environ.setdefault('MFGFORGE_SECRET_KEY', 'superforge-replit-verify')

from superforge_app import create_superforge_app


def main() -> int:
    app = create_superforge_app({'TESTING': True})
    client = app.test_client()
    paths = [
        '/',
        '/company-pulse',
        '/intelligence',
        '/workflows/quote-lead-time-review',
        '/workflows/material-cert-review',
        '/ai-policy',
        '/records/customers',
        '/records/material-certificates/new',
        '/records/machine-utilization/new',
        '/records/supplier-performance/new',
        '/records/quote-intakes/new',
    ]
    failures: list[tuple[str, int]] = []
    for path in paths:
        response = client.get(path)
        if response.status_code != 200:
            failures.append((path, response.status_code))
    if failures:
        for path, status in failures:
            print(f'FAIL {path}: {status}')
        return 1
    print('SuperForge Replit demo verification passed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
