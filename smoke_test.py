from __future__ import annotations

import sqlite3
import tempfile
from pathlib import Path

from app import MODULES, create_app


def assert_ok(response, label: str) -> None:
    assert response.status_code == 200, f'{label} returned {response.status_code}'


def run() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / 'mfgforge_test.sqlite'
        app = create_app({'TESTING': True, 'DATABASE': str(db_path)})
        client = app.test_client()

        response = client.get('/')
        assert_ok(response, 'dashboard')
        assert b'MFGForge' in response.data
        assert b'Quoting' in response.data
        assert b'Planning' in response.data
        assert b'Purchasing' in response.data

        for module in MODULES:
            response = client.get(f"/records/{module['key']}")
            assert_ok(response, f"list {module['key']}")
            assert b'No fake demo data' in response.data

            response = client.get(f"/records/{module['key']}/new")
            assert_ok(response, f"new {module['key']}")

        response = client.post('/records/customers/new', data={'name': 'Smoke Test Customer'}, follow_redirects=True)
        assert_ok(response, 'create customer')
        assert b'Smoke Test Customer' in response.data

        response = client.post('/records/departments/new', data={'name': 'Fabrication'}, follow_redirects=True)
        assert_ok(response, 'create department')
        assert b'Fabrication' in response.data

        response = client.post('/records/suppliers/new', data={'name': 'Smoke Test Supplier'}, follow_redirects=True)
        assert_ok(response, 'create supplier')
        assert b'Smoke Test Supplier' in response.data

        response = client.post('/records/operating-profiles/new', data={'profile_name': 'Hybrid Test', 'operating_mode': 'hybrid'}, follow_redirects=True)
        assert_ok(response, 'create operating profile')
        assert b'Hybrid Test' in response.data

        response = client.get('/records/parts/new')
        assert_ok(response, 'new linked part')
        assert b'Smoke Test Customer' in response.data

        response = client.post('/records/parts/new', data={'part_number': 'SMOKE-PART-001', 'customer_id': '1'}, follow_redirects=True)
        assert_ok(response, 'create linked part')
        assert b'SMOKE-PART-001' in response.data

        response = client.get('/records/materials/new')
        assert_ok(response, 'new material')
        assert b'Smoke Test Supplier' in response.data

        response = client.post('/records/materials/new', data={'material_code': 'MAT-001', 'description': 'Smoke test material', 'supplier_id': '1'}, follow_redirects=True)
        assert_ok(response, 'create material')
        assert b'MAT-001' in response.data

        response = client.get('/records/quote-intakes/new')
        assert_ok(response, 'new quote intake')
        assert b'Smoke Test Customer' in response.data
        assert b'Hybrid Test' in response.data

        response = client.post('/records/quote-intakes/new', data={'quote_number': 'Q-001', 'customer_id': '1', 'operating_profile_id': '1'}, follow_redirects=True)
        assert_ok(response, 'create quote intake')
        assert b'Q-001' in response.data

        response = client.post('/records/pdf-bom-candidates/new', data={'quote_intake_id': '1', 'line_text': '1 EA SMOKE-PART-001 TEST MATERIAL'}, follow_redirects=True)
        assert_ok(response, 'create bom candidate')
        assert b'SMOKE-PART-001' in response.data

        response = client.post('/records/quote-material-drafts/new', data={'quote_intake_id': '1', 'bom_candidate_id': '1', 'material_id': '1', 'pieces_required': '2'}, follow_redirects=True)
        assert_ok(response, 'create material draft')
        assert b'2' in response.data

        response = client.post('/records/morale-snapshots/new', data={'period_start': '2026-01-01', 'period_end': '2026-01-31', 'department_id': '1'}, follow_redirects=True)
        assert_ok(response, 'create morale snapshot')
        assert b'2026-01-01' in response.data

        with sqlite3.connect(db_path) as db:
            part_customer_id = db.execute("SELECT customer_id FROM parts WHERE part_number = 'SMOKE-PART-001'").fetchone()[0]
            material_supplier_id = db.execute("SELECT supplier_id FROM materials WHERE material_code = 'MAT-001'").fetchone()[0]
            quote_customer_id = db.execute("SELECT customer_id FROM quote_intakes WHERE quote_number = 'Q-001'").fetchone()[0]
            morale_department_id = db.execute("SELECT department_id FROM morale_snapshots WHERE period_start = '2026-01-01'").fetchone()[0]
            assert part_customer_id == 1
            assert material_supplier_id == 1
            assert quote_customer_id == 1
            assert morale_department_id == 1

    print('MFGForge smoke test passed.')


if __name__ == '__main__':
    run()
