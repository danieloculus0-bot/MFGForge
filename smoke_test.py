from __future__ import annotations

import tempfile
from pathlib import Path

from app import create_app


def run() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / 'mfgforge_test.sqlite'
        app = create_app({'TESTING': True, 'DATABASE': str(db_path)})
        client = app.test_client()

        response = client.get('/')
        assert response.status_code == 200
        assert b'MFGForge' in response.data

        response = client.get('/records/customers')
        assert response.status_code == 200
        assert b'No records yet' in response.data

        response = client.post('/records/customers/new', data={'name': 'Smoke Test Customer'}, follow_redirects=True)
        assert response.status_code == 200
        assert b'Smoke Test Customer' in response.data

    print('MFGForge smoke test passed.')


if __name__ == '__main__':
    run()
