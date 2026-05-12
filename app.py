from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Any

import click
from flask import Flask, abort, flash, g, redirect, render_template_string, request, url_for

BASE_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = BASE_DIR / 'schema.sql'

def field(name: str, label: str, required: bool = False, kind: str = 'text', source_table: str | None = None, label_column: str | None = None) -> dict[str, Any]:
    return {'name': name, 'label': label, 'required': required, 'kind': kind, 'source_table': source_table, 'label_column': label_column}

MODULES: list[dict[str, Any]] = [
    {'key':'customers','title':'Customers','table':'customers','description':'Customer master records for ERP, quality, work orders, and reporting.','fields':[field('name','Customer name',True),field('code','Customer code'),field('contact_name','Contact name'),field('email','Email',False,'email'),field('phone','Phone'),field('notes','Notes',False,'textarea')]},
    {'key':'suppliers','title':'Suppliers','table':'suppliers','description':'Supplier master records for purchasing, outside processing, and quality follow-up.','fields':[field('name','Supplier name',True),field('code','Supplier code'),field('contact_name','Contact name'),field('email','Email',False,'email'),field('phone','Phone'),field('notes','Notes',False,'textarea')]},
    {'key':'departments','title':'Departments','table':'departments','description':'Shop departments used for scheduling, PM, quality trends, and aggregate morale indicators.','fields':[field('name','Department name',True),field('manager_name','Manager name'),field('notes','Notes',False,'textarea')]},
    {'key':'reason-codes','title':'Reason Codes','table':'reason_codes','description':'Editable reason codes for RMAs, NCRs, DMRs, rejects, deviations, and trend reporting.','fields':[field('code','Code',True),field('label','Label',True),field('category','Category',True),field('notes','Notes',False,'textarea')]},
    {'key':'parts','title':'Parts','table':'parts','description':'Part master foundation for revisions, customer parts, work orders, and quality history.','fields':[field('part_number','Part number',True),field('revision','Revision'),field('customer_id','Customer',False,'select','customers','name'),field('description','Description',False,'textarea'),field('notes','Notes',False,'textarea')]},
    {'key':'work-orders','title':'Work Orders','table':'work_orders','description':'Work order foundation for quantity, due dates, status, and quality linkage.','fields':[field('work_order_number','Work order number',True),field('part_id','Part',False,'select','parts','part_number'),field('customer_id','Customer',False,'select','customers','name'),field('quantity_ordered','Quantity ordered',False,'number'),field('due_date','Due date',False,'date'),field('notes','Notes',False,'textarea')]},
    {'key':'quality-events','title':'Quality Events','table':'quality_events','description':'RMA, NCR, DMR, CAPA, inspection reject, and customer complaint records.','fields':[field('event_type','Event type',True),field('event_number','Event number',True),field('customer_id','Customer',False,'select','customers','name'),field('part_id','Part',False,'select','parts','part_number'),field('work_order_id','Work order',False,'select','work_orders','work_order_number'),field('reason_code_id','Reason code',False,'select','reason_codes','code'),field('quantity_affected','Quantity affected',False,'number'),field('severity','Severity'),field('description','Description',True,'textarea'),field('containment','Containment',False,'textarea'),field('root_cause','Root cause',False,'textarea'),field('corrective_action','Corrective action',False,'textarea'),field('owner','Owner')]},
    {'key':'deviations','title':'Deviation Requests','table':'deviations','description':'Controlled deviation requests with risk assessment and approval status.','fields':[field('deviation_number','Deviation number',True),field('requested_by','Requested by'),field('reason','Reason',True,'textarea'),field('proposed_disposition','Proposed disposition',False,'textarea'),field('risk_assessment','Risk assessment',False,'textarea')]},
    {'key':'documents','title':'Documents','table':'documents','description':'Document control foundation for procedures, drawings, specs, and ERP references.','fields':[field('document_number','Document number',True),field('title','Title',True),field('revision','Revision'),field('document_type','Document type',True),field('owner','Owner'),field('storage_reference','Storage reference'),field('notes','Notes',False,'textarea')]},
    {'key':'pm-assets','title':'PM Assets','table':'pm_assets','description':'Preventive maintenance asset register for equipment, PM frequency, and due dates.','fields':[field('asset_number','Asset number',True),field('name','Asset name',True),field('asset_type','Asset type'),field('pm_frequency','PM frequency'),field('last_pm_date','Last PM date',False,'date'),field('next_pm_date','Next PM date',False,'date'),field('notes','Notes',False,'textarea')]},
    {'key':'morale-snapshots','title':'Morale Snapshots','table':'morale_snapshots','description':'Aggregate-only operational strain records tied to QCDSM risk review.','fields':[field('period_start','Period start',True,'date'),field('period_end','Period end',True,'date'),field('department_id','Department',False,'select','departments','name'),field('overtime_hours','Overtime hours',False,'number'),field('exhausted_pto_count','Exhausted PTO count',False,'number'),field('unscheduled_absence_count','Unscheduled absence count',False,'number'),field('unpaid_timeoff_count','Unpaid time off count',False,'number'),field('turnover_count','Turnover count',False,'number'),field('staffing_notes','Staffing notes',False,'textarea'),field('quality_risk_notes','Quality risk notes',False,'textarea')]},
]
MODULE_BY_KEY = {module['key']: module for module in MODULES}

BASE = """<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>{{ title }}</title><style>:root{color-scheme:dark;--bg:#0b1117;--panel:#111b24;--panel2:#162331;--line:#263747;--text:#e6edf3;--muted:#91a4b7;--accent:#66a3ff}*{box-sizing:border-box}body{margin:0;min-height:100vh;display:grid;grid-template-columns:280px 1fr;background:radial-gradient(circle at top left,#142033 0,var(--bg) 42%);color:var(--text);font-family:Inter,Segoe UI,system-ui,sans-serif}.sidebar{border-right:1px solid var(--line);background:#090f16;padding:24px;position:sticky;top:0;height:100vh}.brand{display:flex;gap:14px;align-items:center;margin-bottom:28px}.mark{width:48px;height:48px;border:1px solid var(--line);border-radius:14px;display:grid;place-items:center;background:var(--panel2);color:var(--accent);font-weight:900}h1,h2,h3,p{margin-top:0}h1{font-size:1.25rem;margin-bottom:2px}p,.muted,.brand p,.card p,.panel p,.hero p,.page-head p{color:var(--muted)}nav{display:grid;gap:8px}nav a,.button{color:var(--text);text-decoration:none;border:1px solid var(--line);background:var(--panel);border-radius:10px;padding:10px 12px;font-weight:700}nav a:hover,.button:hover,.card:hover{border-color:var(--accent)}.content{padding:32px}.hero,.page-head,.panel,.card,.qcard{border:1px solid var(--line);background:rgba(17,27,36,.88);border-radius:18px;box-shadow:0 20px 40px rgba(0,0,0,.18)}.hero,.page-head{padding:28px;margin-bottom:20px}.hero h2,.page-head h2{font-size:clamp(2rem,4vw,3.4rem);margin-bottom:10px;letter-spacing:-.04em}.eyebrow{color:var(--accent);text-transform:uppercase;letter-spacing:.12em;font-size:.78rem;font-weight:900}.grid,.qgrid,.policy{display:grid;gap:14px;margin-bottom:20px}.grid{grid-template-columns:repeat(auto-fill,minmax(260px,1fr))}.qgrid{grid-template-columns:repeat(5,minmax(0,1fr))}.policy{grid-template-columns:repeat(3,minmax(0,1fr))}.qcard,.card,.panel{padding:18px}.qcard span,.count{color:var(--accent);font-size:1.8rem;font-weight:900}.card{display:block;color:var(--text);text-decoration:none}.page-head{display:flex;justify-content:space-between;gap:20px;align-items:center}table{width:100%;border-collapse:collapse;font-size:.92rem}th,td{text-align:left;border-bottom:1px solid var(--line);padding:10px;vertical-align:top}th{color:var(--muted);text-transform:capitalize;font-size:.8rem}.empty{padding:38px;text-align:center;border:1px dashed var(--line);border-radius:14px}.form{display:grid;gap:16px;max-width:860px}label{display:grid;gap:6px;color:var(--muted);font-weight:700}label em{color:var(--accent);font-style:normal;font-size:.8rem}input,textarea,select{width:100%;border:1px solid var(--line);border-radius:10px;background:#071019;color:var(--text);padding:11px 12px;font:inherit}textarea{min-height:110px;resize:vertical}.actions{display:flex;gap:10px}.msg{border:1px solid var(--line);border-radius:10px;padding:10px 12px;background:var(--panel);margin-bottom:8px}@media(max-width:900px){body{grid-template-columns:1fr}.sidebar{position:static;height:auto}.qgrid,.policy{grid-template-columns:1fr}.page-head{display:grid}}</style></head><body><aside class='sidebar'><div class='brand'><div class='mark'>MF</div><div><h1>MFGForge</h1><p>Manufacturing ERP</p></div></div><nav><a href='{{ url_for('dashboard') }}'>Command Center</a>{% for nav_module in modules %}<a href='{{ url_for('list_records', module_key=nav_module.key) }}'>{{ nav_module.title }}</a>{% endfor %}<a href='{{ url_for('ai_policy') }}'>AI Policy</a></nav></aside><main class='content'>{% with messages=get_flashed_messages(with_categories=true) %}{% if messages %}<section>{% for category,message in messages %}<div class='msg {{ category }}'>{{ message }}</div>{% endfor %}</section>{% endif %}{% endwith %}{{ body|safe }}</main></body></html>"""

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
    db.executescript(SCHEMA_PATH.read_text(encoding='utf-8'))
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

def get_select_options(module: dict[str, Any]) -> dict[str, list[sqlite3.Row]]:
    options: dict[str, list[sqlite3.Row]] = {}
    for item in module['fields']:
        if item['kind'] != 'select':
            continue
        rows = get_db().execute(f"SELECT id, {item['label_column']} AS label FROM {item['source_table']} ORDER BY {item['label_column']}").fetchall()
        options[item['name']] = rows
    return options

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
        if module_key not in MODULE_BY_KEY:
            abort(404)
        module = MODULE_BY_KEY[module_key]
        rows = get_db().execute(f"SELECT * FROM {module['table']} ORDER BY id DESC LIMIT 100").fetchall()
        body = render_template_string("""<section class='page-head'><div><p class='eyebrow'>Records</p><h2>{{ module.title }}</h2><p>{{ module.description }}</p></div><a class='button' href='{{ url_for('create_record', module_key=module.key) }}'>New Record</a></section><section class='panel'>{% if rows %}<table><thead><tr>{% for key in rows[0].keys() %}<th>{{ key.replace('_',' ') }}</th>{% endfor %}</tr></thead><tbody>{% for row in rows %}<tr>{% for key in row.keys() %}<td>{{ row[key] }}</td>{% endfor %}</tr>{% endfor %}</tbody></table>{% else %}<div class='empty'><h3>No records yet.</h3><p>This module is ready for real records. No fake demo data has been inserted.</p></div>{% endif %}</section>""", module=module, rows=rows)
        return page(f"{module['title']} | MFGForge", body)

    @app.route('/records/<module_key>/new', methods=('GET', 'POST'))
    def create_record(module_key: str) -> str:
        if module_key not in MODULE_BY_KEY:
            abort(404)
        module = MODULE_BY_KEY[module_key]
        select_options = get_select_options(module)
        if request.method == 'POST':
            values: dict[str, Any] = {}
            errors: list[str] = []
            for item in module['fields']:
                value = request.form.get(item['name'], '').strip()
                if item['required'] and not value:
                    errors.append(f"{item['label']} is required.")
                if value:
                    values[item['name']] = int(value) if item['kind'] == 'select' else value
            if module['table'] == 'quality_events' and 'severity' not in values:
                values['severity'] = 'unassigned'
            if errors:
                for error in errors:
                    flash(error, 'error')
            else:
                insert_record(module['table'], values)
                flash(f"{module['title']} record created.", 'success')
                return redirect(url_for('list_records', module_key=module['key']))
        body = render_template_string("""<section class='page-head'><div><p class='eyebrow'>Create record</p><h2>New {{ module.title }}</h2><p>{{ module.description }}</p></div></section><form class='panel form' method='post'>{% for item in module.fields %}<label><span>{{ item.label }}{% if item.required %} <em>required</em>{% endif %}</span>{% if item.kind == 'textarea' %}<textarea name='{{ item.name }}' {% if item.required %}required{% endif %}></textarea>{% elif item.kind == 'select' %}<select name='{{ item.name }}'><option value=''>No linked record</option>{% for option in select_options[item.name] %}<option value='{{ option.id }}'>{{ option.label }}</option>{% endfor %}</select>{% else %}<input type='{{ item.kind }}' name='{{ item.name }}' {% if item.required %}required{% endif %}>{% endif %}</label>{% endfor %}<div class='actions'><button class='button' type='submit'>Save record</button><a class='button' href='{{ url_for('list_records', module_key=module.key) }}'>Cancel</a></div></form>""", module=module, select_options=select_options)
        return page(f"New {module['title']} | MFGForge", body)

    @app.get('/ai-policy')
    def ai_policy() -> str:
        body = """<section class='page-head'><div><p class='eyebrow'>Human-in-the-loop</p><h2>AI acts like GPS, not a self-driving car.</h2><p>AI assistance may analyze, draft, summarize, and recommend. Business-critical execution requires human approval and audit logging.</p></div></section><section class='policy'><article class='panel'><h3>Allowed assistance</h3><p>Summarize trends, draft quality language, flag risks, explain records, suggest next actions, and prepare reports from approved data.</p></article><article class='panel'><h3>Approval required</h3><p>Closing quality records, changing inventory, releasing jobs, approving deviations, editing customer records, or sending external communications.</p></article><article class='panel'><h3>Audit path</h3><p>Read-only analysis, draft recommendation, human approval, logged execution, and traceable review history.</p></article></section>"""
        return page('AI Policy | MFGForge', body)

if __name__ == '__main__':
    create_app().run(debug=True)
