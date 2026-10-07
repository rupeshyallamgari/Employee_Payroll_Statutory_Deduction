PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS departments (
 department_id INTEGER PRIMARY KEY AUTOINCREMENT,
 department_name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS employees (
 employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
 employee_code TEXT NOT NULL UNIQUE,
 first_name TEXT NOT NULL,
 last_name TEXT NOT NULL,
 email TEXT,
 phone TEXT,
 department_id INTEGER,
 designation TEXT NOT NULL,
 joining_date TEXT NOT NULL,
 basic_salary REAL NOT NULL CHECK(basic_salary >= 0),
 status TEXT NOT NULL DEFAULT 'Active',
 FOREIGN KEY(department_id) REFERENCES departments(department_id) ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS payroll (
 payroll_id INTEGER PRIMARY KEY AUTOINCREMENT,
 employee_id INTEGER NOT NULL,
 pay_month TEXT NOT NULL,
 basic_salary REAL NOT NULL,
 hra REAL NOT NULL DEFAULT 0,
 allowance REAL NOT NULL DEFAULT 0,
 bonus REAL NOT NULL DEFAULT 0,
 gross_salary REAL NOT NULL,
 pf REAL NOT NULL DEFAULT 0,
 esi REAL NOT NULL DEFAULT 0,
 professional_tax REAL NOT NULL DEFAULT 0,
 tds REAL NOT NULL DEFAULT 0,
 total_deductions REAL NOT NULL,
 net_salary REAL NOT NULL,
 status TEXT NOT NULL DEFAULT 'Processed',
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY(employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE
);
