from __future__ import annotations

import sqlite3
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

        response = client.get('/records/parts/new')
        assert response.status_code == 200
        assert b'No linked record' in response.data

        response = client.get('/records/work-orders/new')
        assert response.status_code == 200
        assert b'No linked record' in response.data

        response = client.get('/records/quality-events/new')
        assert response.status_code == 200
        assert b'No linked record' in response.data

        response = client.post('/records/customers/new', data={'name': 'Smoke Test Customer'}, follow_redirects=True)
        assert response.status_code == 200
        assert b'Smoke Test Customer' in response.data

        response = client.get('/records/parts/new')
        assert response.status_code == 200
        assert b'Smoke Test Customer' in response.data

        response = client.post('/records/parts/new', data={'part_number': 'SMOKE-PART-001', 'customer_id': '1'}, follow_redirects=True)
        assert response.status_code == 200
        assert b'SMOKE-PART-001' in response.data

        with sqlite3.connect(db_path) as db:
            customer_id = db.execute("SELECT customer_id FROM parts WHERE part_number = 'SMOKE-PART-001'").fetchone()[0]
            assert customer_id == 1

    print('MFGForge smoke test passed.')


if __name__ == '__main__':
    run()
