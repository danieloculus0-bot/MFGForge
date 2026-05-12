CREATE TABLE IF NOT EXISTS system_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    code TEXT,
    contact_name TEXT,
    email TEXT,
    phone TEXT,
    status TEXT NOT NULL DEFAULT 'active',
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    code TEXT,
    contact_name TEXT,
    email TEXT,
    phone TEXT,
    status TEXT NOT NULL DEFAULT 'active',
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    manager_name TEXT,
    status TEXT NOT NULL DEFAULT 'active',
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reason_codes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    label TEXT NOT NULL,
    category TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS parts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    part_number TEXT NOT NULL UNIQUE,
    revision TEXT,
    description TEXT,
    customer_id INTEGER REFERENCES customers(id),
    status TEXT NOT NULL DEFAULT 'active',
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS work_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    work_order_number TEXT NOT NULL UNIQUE,
    part_id INTEGER REFERENCES parts(id),
    customer_id INTEGER REFERENCES customers(id),
    quantity_ordered INTEGER,
    due_date TEXT,
    status TEXT NOT NULL DEFAULT 'open',
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS quality_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL CHECK (event_type IN ('RMA', 'NCR', 'DMR', 'CAPA', 'INSPECTION_REJECT', 'CUSTOMER_COMPLAINT')),
    event_number TEXT NOT NULL UNIQUE,
    customer_id INTEGER REFERENCES customers(id),
    part_id INTEGER REFERENCES parts(id),
    work_order_id INTEGER REFERENCES work_orders(id),
    reason_code_id INTEGER REFERENCES reason_codes(id),
    quantity_affected INTEGER,
    severity TEXT NOT NULL DEFAULT 'unassigned',
    status TEXT NOT NULL DEFAULT 'open',
    description TEXT NOT NULL,
    containment TEXT,
    root_cause TEXT,
    corrective_action TEXT,
    owner TEXT,
    opened_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    closed_at TEXT,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS deviations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    deviation_number TEXT NOT NULL UNIQUE,
    customer_id INTEGER REFERENCES customers(id),
    part_id INTEGER REFERENCES parts(id),
    work_order_id INTEGER REFERENCES work_orders(id),
    requested_by TEXT,
    reason TEXT NOT NULL,
    proposed_disposition TEXT,
    risk_assessment TEXT,
    approval_status TEXT NOT NULL DEFAULT 'draft',
    status TEXT NOT NULL DEFAULT 'open',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    closed_at TEXT
);

CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_number TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    revision TEXT,
    document_type TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'draft',
    owner TEXT,
    storage_reference TEXT,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pm_assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_number TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    department_id INTEGER REFERENCES departments(id),
    asset_type TEXT,
    status TEXT NOT NULL DEFAULT 'active',
    pm_frequency TEXT,
    last_pm_date TEXT,
    next_pm_date TEXT,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS morale_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    period_start TEXT NOT NULL,
    period_end TEXT NOT NULL,
    department_id INTEGER REFERENCES departments(id),
    overtime_hours REAL,
    exhausted_pto_count INTEGER,
    unscheduled_absence_count INTEGER,
    unpaid_timeoff_count INTEGER,
    turnover_count INTEGER,
    staffing_notes TEXT,
    quality_risk_notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ai_action_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action_type TEXT NOT NULL,
    target_table TEXT,
    target_id INTEGER,
    prompt_summary TEXT NOT NULL,
    recommendation TEXT,
    human_approval_status TEXT NOT NULL DEFAULT 'draft',
    executed_at TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO system_meta (key, value) VALUES ('schema_version', '0.1.0');
