from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Any

import click
from flask import Flask, flash, g, redirect, render_template_string, request, url_for

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS system_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, code TEXT, contact_name TEXT, email TEXT, phone TEXT, status TEXT NOT NULL DEFAULT 'active', notes TEXT, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS suppliers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, code TEXT, contact_name TEXT, email TEXT, phone TEXT, status TEXT NOT NULL DEFAULT 'active', notes TEXT, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS departments (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, manager_name TEXT, status TEXT NOT NULL DEFAULT 'active', notes TEXT, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS reason_codes (id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT NOT NULL UNIQUE, label TEXT NOT NULL, category TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'active', notes TEXT, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS parts (id INTEGER PRIMARY KEY AUTOINCREMENT, part_number TEXT NOT NULL UNIQUE, revision TEXT, description TEXT, customer_id INTEGER REFERENCES customers(id), status TEXT NOT NULL DEFAULT 'active', notes TEXT, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS work_orders (id INTEGER PRIMARY KEY AUTOINCREMENT, work_order_number TEXT NOT NULL UNIQUE, part_id INTEGER REFERENCES parts(id), customer_id INTEGER REFERENCES customers(id), quantity_ordered INTEGER, due_date TEXT, status TEXT NOT NULL DEFAULT 'open', notes TEXT, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS quality_events (id INTEGER PRIMARY KEY AUTOINCREMENT, event_type TEXT NOT NULL CHECK (event_type IN ('RMA', 'NCR', 'DMR', 'CAPA', 'INSPECTION_REJECT', 'CUSTOMER_COMPLAINT')), event_number TEXT NOT NULL UNIQUE, customer_id INTEGER REFERENCES customers(id), part_id INTEGER REFERENCES parts(id), work_order_id INTEGER REFERENCES work_orders(id), reason_code_id INTEGER REFERENCES reason_codes(id), quantity_affected INTEGER, severity TEXT NOT NULL DEFAULT 'unassigned', status TEXT NOT NULL DEFAULT 'open', description TEXT NOT NULL, containment TEXT, root_cause TEXT, corrective_action TEXT, owner TEXT, opened_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, closed_at TEXT, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS deviations (id INTEGER PRIMARY KEY AUTOINCREMENT, deviation_number TEXT NOT NULL UNIQUE, customer_id INTEGER REFERENCES customers(id), part_id INTEGER REFERENCES parts(id), work_order_id INTEGER REFERENCES work_orders(id), requested_by TEXT, reason TEXT NOT NULL, proposed_disposition TEXT, risk_assessment TEXT, approval_status TEXT NOT NULL DEFAULT 'draft', status TEXT NOT NULL DEFAULT 'open', created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, closed_at TEXT);
CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY AUTOINCREMENT, document_number TEXT NOT NULL UNIQUE, title TEXT NOT NULL, revision TEXT, document_type TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'draft', owner TEXT, storage_reference TEXT, notes TEXT, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS pm_assets (id INTEGER PRIMARY KEY AUTOINCREMENT, asset_number TEXT NOT NULL UNIQUE, name TEXT NOT NULL, department_id INTEGER REFERENCES departments(id), asset_type TEXT, status TEXT NOT NULL DEFAULT 'active', pm_frequency TEXT, last_pm_date TEXT, next_pm_date TEXT, notes TEXT, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS morale_snapshots (id INTEGER PRIMARY KEY AUTOINCREMENT, period_start TEXT NOT NULL, period_end TEXT NOT NULL, department_id INTEGER REFERENCES departments(id), overtime_hours REAL, exhausted_pto_count INTEGER, unscheduled_absence_count INTEGER, unpaid_timeoff_count INTEGER, turnover_count INTEGER, staffing_notes TEXT, quality_risk_notes TEXT, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS ai_action_log (id INTEGER PRIMARY KEY AUTOINCREMENT, action_type TEXT NOT NULL, target_table TEXT, target_id INTEGER, prompt_summary TEXT NOT NULL, recommendation TEXT, human_approval_status TEXT NOT NULL DEFAULT 'draft', executed_at TEXT, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
INSERT OR IGNORE INTO system_meta (key, value) VALUES ('schema_version', '0.1.0');
"""

MODULES: list[dict[str, Any]] = [
    {'key':'customers','title':'Customers','table':'customers','description':'Customer master records for ERP, quality, work orders, and reporting.','fields':[('name','Customer name',True,'text'),('code','Customer code',False,'text'),('contact_name','Contact name',False,'text'),('email','Email',False,'email'),('phone','Phone',False,'text'),('notes','Notes',False,'textarea')]},
    {'key':'suppliers','title':'Suppliers','table':'suppliers','description':'Supplier master records for purchasing, outside processing, and quality follow-up.','fields':[('name','Supplier name',True,'text'),('code','Supplier code',False,'text'),('contact_name','Contact name',False,'text'),('email','Email',False,'email'),('phone','Phone',False,'text'),('notes','Notes',False,'textarea')]},
    {'key':'departments','title':'Departments','table':'departments','description':'Shop departments used for scheduling, PM, quality trends, and aggregate morale indicators.','fields':[('name','Department name',True,'text'),('manager_name','Manager name',False,'text'),('notes','Notes',False,'textarea')]},
    {'key':'reason-codes','title':'Reason Codes','table':'reason_codes','description':'Editable reason codes for RMAs, NCRs, DMRs, rejects, deviations, and trend reporting.','fields':[('code','Code',True,'text'),('label','Label',True,'text'),('category','Category',True,'text'),('notes','Notes',False,'textarea')]},
    {'key':'parts','title':'Parts','table':'parts','description':'Part master foundation for revisions, customer parts, work orders, and quality history.','fields':[('part_number','Part number',True,'text'),('revision','Revision',False,'text'),('description','Description',False,'textarea'),('notes','Notes',False,'textarea')]},
    {'key':'work-orders','title':'Work Orders','table':'work_orders','description':'Work order foundation for quantity, due dates, status, and quality linkage.','fields':[('work_order_number','Work order number',True,'text'),('quantity_ordered','Quantity ordered',False,'number'),('due_date','Due date',False,'date'),('notes','Notes',False,'textarea')]},
    {'key':'quality-events','title':'Quality Events','table':'quality_events','description':'RMA, NCR, DMR, CAPA, inspection reject, and customer complaint records.','fields':[('event_type','Event type',True,'text'),('event_number','Event number',True,'text'),('quantity_affected','Quantity affected',False,'number'),('severity','Severity',False,'text'),('description','Description',True,'textarea'),('containment','Containment',False,'textarea'),('root_cause','Root cause',False,'textarea'),('corrective_action','Corrective action',False,'textarea'),('owner','Owner',False,'text')]},
    {'key':'deviations','title':'Deviation Requests','table':'deviations','description':'Controlled deviation requests with risk assessment and approval status.','fields':[('deviation_number','Deviation number',True,'text'),('requested_by','Requested by',False,'text'),('reason','Reason',True,'textarea'),('proposed_disposition','Proposed disposition',False,'textarea'),('risk_assessment','Risk assessment',False,'textarea')]},
    {'key':'documents','title':'Documents','table':'documents','description':'Document control foundation for procedures, drawings, specs, and ERP references.','fields':[('document_number','Document number',True,'text'),('title','Title',True,'text'),('revision','Revision',False,'text'),('document_type','Document type',True,'text'),('owner','Owner',False,'text'),('storage_reference','Storage reference',False,'text'),('notes','Notes',False,'textarea')]},
    {'key':'pm-assets','title':'PM Assets','table':'pm_assets','description':'Preventive maintenance asset register for equipment, PM frequency, and due dates.','fields':[('asset_number','Asset number',True,'text'),('name','Asset name',True,'text'),('asset_type','Asset type',False,'text'),('pm_frequency','PM frequency',False,'text'),('last_pm_date','Last PM date',False,'date'),('next_pm_date','Next PM date',False,'date'),('notes','Notes',False,'textarea')]},
    {'key':'morale-snapshots','title':'Morale Snapshots','table':'morale_snapshots','description':'Aggregate-only operational strain records tied to QCDSM risk review.','fields':[('period_start','Period start',True,'date'),('period_end','Period end',True,'date'),('overtime_hours','Overtime hours',False,'number'),('exhausted_pto_count','Exhausted PTO count',False,'number'),('unscheduled_absence_count','Unscheduled absence count',False,'number'),('unpaid_timeoff_count','Unpaid time off count',False,'number'),('turnover_count','Turnover count',False,'number'),('staffing_notes','Staffing notes',False,'textarea'),('quality_risk_notes','Quality risk notes',False,'textarea')]},
]
MODULE_BY_KEY = {module['key']: module for module in MODULES}

BASE = """<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>{{ title }}</title><style>:root{color-scheme:dark;--bg:#0b1117;--panel:#111b24;--panel2:#162331;--line:#263747;--text:#e6edf3;--muted:#91a4b7;--accent:#66a3ff}*{box-sizing:border-box}body{margin:0;min-height:100vh;display:grid;grid-template-columns:280px 1fr;background:radial-gradient(circle at top left,#142033 0,var(--bg) 42%);color:var(--text);font-family:Inter,Segoe UI,system-ui,sans-serif}.sidebar{border-right:1px solid var(--line);background:#090f16;padding:24px;position:sticky;top:0;height:100vh}.brand{display:flex;gap:14px;align-items:center;margin-bottom:28px}.mark{width:48px;height:48px;border:1px solid var(--line);border-radius:14px;display:grid;place-items:center;background:var(--panel2);color:var(--accent);font-weight:900}h1,h2,h3,p{margin-top:0}h1{font-size:1.25rem;margin-bottom:2px}p,.muted,.brand p,.card p,.panel p,.hero p,.page-head p{color:var(--muted)}nav{display:grid;gap:8px}nav a,.button{color:var(--text);text-decoration:none;border:1px solid var(--line);background:var(--panel);border-radius:10px;padding:10px 12px;font-weight:700}nav a:hover,.button:hover,.card:hover{border-color:var(--accent)}.content{padding:32px}.hero,.page-head,.panel,.card,.qcard{border:1px solid var(--line);background:rgba(17,27,36,.88);border-radius:18px;box-shadow:0 20px 40px rgba(0,0,0,.18)}.hero,.page-head{padding:28px;margin-bottom:20px}.hero h2,.page-head h2{font-size:clamp(2rem,4vw,3.4rem);margin-bottom:10px;letter-spacing:-.04em}.eyebrow{color:var(--accent);text-transform:uppercase;letter-spacing:.12em;font-size:.78rem;font-weight:900}.grid,.qgrid,.policy{display:grid;gap:14px;margin-bottom:20px}.grid{grid-template-columns:repeat(auto-fill,minmax(260px,1fr))}.qgrid{grid-template-columns:repeat(5,minmax(0,1fr))}.policy{grid-template-columns:repeat(3,minmax(0,1fr))}.qcard,.card,.panel{padding:18px}.qcard span,.count{color:var(--accent);font-size:1.8rem;font-weight:900}.card{display:block;color:var(--text);text-decoration:none}.page-head{display:flex;justify-content:space-between;gap:20px;align-items:center}table{width:100%;border-collapse:collapse;font-size:.92rem}th,td{text-align:left;border-bottom:1px solid var(--line);padding:10px;vertical-align:top}th{color:var(--muted);text-transform:capitalize;font-size:.8rem}.empty{padding:38px;text-align:center;border:1px dashed var(--line);border-radius:14px}.form{display:grid;gap:16px;max-width:860px}label{display:grid;gap:6px;color:var(--muted);font-weight:700}label em{color:var(--accent);font-style:normal;font-size:.8rem}input,textarea{width:100%;border:1px solid var(--line);border-radius:10px;background:#071019;color:var(--text);padding:11px 12px;font:inherit}textarea{min-height:110px;resize:vertical}.actions{display:flex;gap:10px}.msg{border:1px solid var(--line);border-radius:10px;padding:10px 12px;background:var(--panel);margin-bottom:8px}@media(max-width:900px){body{grid-template-columns:1fr}.sidebar{position:static;height:auto}.qgrid,.policy{grid-template-columns:1fr}.page-head{display:grid}}</style></head><body><aside class='sidebar'><div class='brand'><div class='mark'>MF</div><div><h1>MFGForge</h1><p>Manufacturing ERP</p></div></div><nav><a href='{{ url_for('dashboard') }}'>Command Center</a>{% for nav_module in modules %}<a href='{{ url_for('list_records', module_key=nav_module.key) }}'>{{ nav_module.title }}</a>{% endfor %}<a href='{{ url_for('ai_policy') }}'>AI Policy</a></nav></aside><main class='content'>{% with messages=get_flashed_messages(with_categories=true) %}{% if messages %}<section>{% for category,message in messages %}<div class='msg {{ category }}'>{{ message }}</div>{% endfor %}</section>{% endif %}{% endwith %}{{ body|safe }}</main></body></html>"""

def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY=os.environ.get('MFGFORGE_SECRET_KEY', 'dev-change-me'), DATABASE=str(Path(app.instance_path) / 'mfgforge.sqlite'))
    if test_config:
        app.config.update(test_config)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    register_routes(app)
    with app.app_context():
        ensure_database()
    return app

def get_db() -> sqlite3.Connection:
    if 'db' not in g:
        from flask import current_app
        database_path = Path(current_app.config['DATABASE'])
        database_path.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(database_path)
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys = ON')
    return g.db

def close_db(error: Exception | None = None) -> None:
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db() -> None:
    db = get_db()
    db.executescript(SCHEMA_SQL)
    db.commit()

def ensure_database() -> None:
    existing = get_db().execute("SELECT name FROM sqlite_master WHERE type='table' AND name='system_meta'").fetchone()
    if existing is None:
        init_db()

@click.command('init-db')
def init_db_command() -> None:
    init_db()
    click.echo('Initialized MFGForge database.')

def table_count(table_name: str) -> int:
    row = get_db().execute(f'SELECT COUNT(*) AS count FROM {table_name}').fetchone()
    return int(row['count'])

def insert_record(table_name: str, values: dict[str, Any]) -> int:
    columns = ', '.join(values.keys())
    placeholders = ', '.join('?' for _ in values)
    cursor = get_db().execute(f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})', list(values.values()))
    get_db().commit()
    return int(cursor.lastrowid)

def page(title: str, body: str) -> str:
    return render_template_string(BASE, title=title, modules=MODULES, body=body)

def register_routes(app: Flask) -> None:
    @app.get('/')
    def dashboard() -> str:
        counts = {module['key']: table_count(module['table']) for module in MODULES}
        body = render_template_string("""<section class='hero'><p class='eyebrow'>QCDSM ERP Foundation</p><h2>Manufacturing command center</h2><p>MFGForge is the unified ERP shell for quality, cost, delivery, safety, morale, planning, maintenance, documents, and approval-gated AI assistance.</p></section><section class='qgrid'><article class='qcard'><span>Q</span><strong>Quality</strong><p>RMA, NCR, DMR, CAPA, inspection rejects, deviations.</p></article><article class='qcard'><span>C</span><strong>Cost</strong><p>Part, work order, supplier, and quote intelligence foundation.</p></article><article class='qcard'><span>D</span><strong>Delivery</strong><p>Work orders, due dates, PM risk, document readiness.</p></article><article class='qcard'><span>S</span><strong>Safety</strong><p>Controlled records and audit-ready escalation paths.</p></article><article class='qcard'><span>M</span><strong>Morale</strong><p>Aggregate strain indicators tied to operational risk.</p></article></section><section class='grid'>{% for module in modules %}<a class='card' href='{{ url_for('list_records', module_key=module.key) }}'><span class='count'>{{ counts[module.key] }}</span><h3>{{ module.title }}</h3><p>{{ module.description }}</p></a>{% endfor %}</section>""", modules=MODULES, counts=counts)
        return page('MFGForge Command Center', body)

    @app.get('/records/<module_key>')
    def list_records(module_key: str) -> str:
        module = MODULE_BY_KEY[module_key]
        rows = get_db().execute(f"SELECT * FROM {module['table']} ORDER BY id DESC LIMIT 100").fetchall()
        body = render_template_string("""<section class='page-head'><div><p class='eyebrow'>Records</p><h2>{{ module.title }}</h2><p>{{ module.description }}</p></div><a class='button' href='{{ url_for('create_record', module_key=module.key) }}'>New Record</a></section><section class='panel'>{% if rows %}<table><thead><tr>{% for key in rows[0].keys() %}<th>{{ key.replace('_',' ') }}</th>{% endfor %}</tr></thead><tbody>{% for row in rows %}<tr>{% for key in row.keys() %}<td>{{ row[key] }}</td>{% endfor %}</tr>{% endfor %}</tbody></table>{% else %}<div class='empty'><h3>No records yet.</h3><p>This module is ready for real records. No fake demo data has been inserted.</p></div>{% endif %}</section>""", module=module, rows=rows)
        return page(f"{module['title']} | MFGForge", body)

    @app.route('/records/<module_key>/new', methods=('GET', 'POST'))
    def create_record(module_key: str) -> str:
        module = MODULE_BY_KEY[module_key]
        if request.method == 'POST':
            values: dict[str, Any] = {}
            errors: list[str] = []
            for name, label, required, field_type in module['fields']:
                value = request.form.get(name, '').strip()
                if required and not value:
                    errors.append(f'{label} is required.')
                if value:
                    values[name] = value
            if module['table'] == 'quality_events' and 'severity' not in values:
                values['severity'] = 'unassigned'
            if errors:
                for error in errors:
                    flash(error, 'error')
            else:
                insert_record(module['table'], values)
                flash(f"{module['title']} record created.", 'success')
                return redirect(url_for('list_records', module_key=module['key']))
        body = render_template_string("""<section class='page-head'><div><p class='eyebrow'>Create record</p><h2>New {{ module.title }}</h2><p>{{ module.description }}</p></div></section><form class='panel form' method='post'>{% for name,label,required,field_type in module.fields %}<label><span>{{ label }}{% if required %} <em>required</em>{% endif %}</span>{% if field_type == 'textarea' %}<textarea name='{{ name }}' {% if required %}required{% endif %}></textarea>{% else %}<input type='{{ field_type }}' name='{{ name }}' {% if required %}required{% endif %}>{% endif %}</label>{% endfor %}<div class='actions'><button class='button' type='submit'>Save record</button><a class='button' href='{{ url_for('list_records', module_key=module.key) }}'>Cancel</a></div></form>""", module=module)
        return page(f"New {module['title']} | MFGForge", body)

    @app.get('/ai-policy')
    def ai_policy() -> str:
        body = """<section class='page-head'><div><p class='eyebrow'>Human-in-the-loop</p><h2>AI acts like GPS, not a self-driving car.</h2><p>AI assistance may analyze, draft, summarize, and recommend. Business-critical execution requires human approval and audit logging.</p></div></section><section class='policy'><article class='panel'><h3>Allowed assistance</h3><p>Summarize trends, draft quality language, flag risks, explain records, suggest next actions, and prepare reports from approved data.</p></article><article class='panel'><h3>Approval required</h3><p>Closing quality records, changing inventory, releasing jobs, approving deviations, editing customer records, or sending external communications.</p></article><article class='panel'><h3>Audit path</h3><p>Read-only analysis, draft recommendation, human approval, logged execution, and traceable review history.</p></article></section>"""
        return page('AI Policy | MFGForge', body)

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
