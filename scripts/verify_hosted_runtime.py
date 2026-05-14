from __future__ import annotations

import os
import tempfile
from pathlib import Path

from superforge_app import create_superforge_app


REQUIRED_ROUTES = [
    '/',
    '/company-pulse',
    '/intelligence',
    '/ai-policy',
    '/records/customers',
    '/records/material-certificates/new',
]

OPTIONAL_WORKFLOW_ROUTES = [
    '/workflows/quote-lead-time-review',
    '/workflows/material-cert-review',
]


def assert_ok(client, route: str) -> None:
    response = client.get(route)
    if response.status_code != 200:
        body = response.get_data(as_text=True)[:500]
        raise AssertionError(f'{route} returned {response.status_code}: {body}')


def main() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / 'superforge_hosted_runtime.sqlite'
        os.environ['MFGFORGE_DATABASE'] = str(db_path)
        os.environ['MFGFORGE_SECRET_KEY'] = 'hosted-runtime-verification'
        app = create_superforge_app()
        app.config.update(TESTING=True)

        with app.test_client() as client:
            for route in REQUIRED_ROUTES:
                assert_ok(client, route)

            for route in OPTIONAL_WORKFLOW_ROUTES:
                response = client.get(route)
                if response.status_code not in {200, 404}:
                    body = response.get_data(as_text=True)[:500]
                    raise AssertionError(f'{route} returned {response.status_code}: {body}')

    print('Hosted runtime verification passed.')


if __name__ == '__main__':
    main()
