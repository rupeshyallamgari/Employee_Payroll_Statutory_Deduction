from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path
from datetime import date

BASE_DIR = Path(__file__).resolve().parent
DB = BASE_DIR / 'database' / 'payroll.db'
app = Flask(__name__)
app.secret_key = 'payroll-demo-secret-key'


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db():
    DB.parent.mkdir(exist_ok=True)
    conn = get_db()
    schema = (BASE_DIR / 'database' / 'schema.sql').read_text(encoding='utf-8')
    conn.executescript(schema)
    count = conn.execute('SELECT COUNT(*) FROM employees').fetchone()[0]
    if count == 0:
        seed = (BASE_DIR / 'database' / 'seed.sql').read_text(encoding='utf-8')
        conn.executescript(seed)
    conn.commit()
    conn.close()


def calculate_gross(basic, hra, allowance, bonus):
    return round(basic + hra + allowance + bonus, 2)


def calculate_deductions(gross, pf_rate=12, esi_rate=0.75, pt=200, tds=0):
    pf = round(gross * pf_rate / 100, 2)
    esi = round(gross * esi_rate / 100, 2)
    tds_val = round(float(tds), 2)
    total = round(pf + esi + pt + tds_val, 2)
    net = round(gross - total, 2)
    return pf, esi, float(pt), tds_val, total, net


@app.route('/')
def dashboard():
    conn = get_db()
    stats = {
        'employees': conn.execute('SELECT COUNT(*) FROM employees WHERE status="Active"').fetchone()[0],
        'payrolls': conn.execute('SELECT COUNT(*) FROM payroll').fetchone()[0],
        'gross': conn.execute('SELECT COALESCE(SUM(gross_salary),0) FROM payroll').fetchone()[0],
        'deductions': conn.execute('SELECT COALESCE(SUM(total_deductions),0) FROM payroll').fetchone()[0],
    }
    recent = conn.execute('''SELECT p.*, e.employee_code, e.first_name, e.last_name
                             FROM payroll p JOIN employees e ON e.employee_id=p.employee_id
                             ORDER BY p.payroll_id DESC LIMIT 6''').fetchall()
    conn.close()
    return render_template('dashboard.html', stats=stats, recent=recent)


@app.route('/employees')
def employees():
    conn = get_db()
    rows = conn.execute('''SELECT e.*, d.department_name FROM employees e
                           LEFT JOIN departments d ON d.department_id=e.department_id
                           ORDER BY e.employee_id DESC''').fetchall()
    departments = conn.execute('SELECT * FROM departments ORDER BY department_name').fetchall()
    conn.close()
    return render_template('employees.html', employees=rows, departments=departments)


@app.route('/employees/add', methods=['POST'])
def add_employee():
    f = request.form
    try:
        conn = get_db()
        conn.execute('''INSERT INTO employees(employee_code, first_name, last_name, email, phone,
                       department_id, designation, joining_date, basic_salary, status)
                       VALUES (?,?,?,?,?,?,?,?,?,?)''', (
            f['employee_code'], f['first_name'], f['last_name'], f['email'], f['phone'],
            f.get('department_id') or None, f['designation'], f['joining_date'],
            float(f['basic_salary']), f.get('status','Active')
        ))
        conn.commit(); conn.close()
        flash('Employee added successfully.', 'success')
    except sqlite3.IntegrityError:
        flash('Employee code already exists. Use a unique code.', 'error')
    return redirect(url_for('employees'))


@app.route('/employees/delete/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    conn = get_db()
    conn.execute('DELETE FROM employees WHERE employee_id=?', (employee_id,))
    conn.commit(); conn.close()
    flash('Employee deleted.', 'success')
    return redirect(url_for('employees'))


@app.route('/payroll')
def payroll():
    conn = get_db()
    rows = conn.execute('''SELECT p.*, e.employee_code, e.first_name, e.last_name
                           FROM payroll p JOIN employees e ON e.employee_id=p.employee_id
                           ORDER BY p.payroll_id DESC''').fetchall()
    emps = conn.execute('SELECT * FROM employees WHERE status="Active" ORDER BY first_name').fetchall()
    conn.close()
    return render_template('payroll.html', payrolls=rows, employees=emps, today=date.today().isoformat())


@app.route('/payroll/generate', methods=['POST'])
def generate_payroll():
    f = request.form
    conn = get_db()
    emp = conn.execute('SELECT * FROM employees WHERE employee_id=?', (f['employee_id'],)).fetchone()
    if not emp:
        flash('Employee not found.', 'error'); conn.close(); return redirect(url_for('payroll'))
    basic = float(emp['basic_salary'])
    hra = float(f.get('hra') or basic * 0.40)
    allowance = float(f.get('allowance') or 0)
    bonus = float(f.get('bonus') or 0)
    gross = calculate_gross(basic, hra, allowance, bonus)
    pf_rate = float(f.get('pf_rate') or 12)
    esi_rate = float(f.get('esi_rate') or 0.75)
    pt = float(f.get('professional_tax') or 200)
    tds = float(f.get('tds') or 0)
    pf, esi, pt, tds, total, net = calculate_deductions(gross, pf_rate, esi_rate, pt, tds)
    conn.execute('''INSERT INTO payroll(employee_id, pay_month, basic_salary, hra, allowance, bonus,
                   gross_salary, pf, esi, professional_tax, tds, total_deductions, net_salary, status)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                 (emp['employee_id'], f['pay_month'], basic, hra, allowance, bonus, gross,
                  pf, esi, pt, tds, total, net, 'Processed'))
    conn.commit(); conn.close()
    flash('Payroll generated successfully.', 'success')
    return redirect(url_for('payroll'))


@app.route('/deductions')
def deductions():
    conn = get_db()
    rows = conn.execute('''SELECT p.*, e.employee_code, e.first_name, e.last_name
                           FROM payroll p JOIN employees e ON e.employee_id=p.employee_id
                           ORDER BY p.payroll_id DESC''').fetchall()
    totals = conn.execute('''SELECT COALESCE(SUM(pf),0) pf, COALESCE(SUM(esi),0) esi,
                             COALESCE(SUM(professional_tax),0) pt, COALESCE(SUM(tds),0) tds,
                             COALESCE(SUM(total_deductions),0) total FROM payroll''').fetchone()
    conn.close()
    return render_template('deductions.html', rows=rows, totals=totals)


@app.route('/reports')
def reports():
    conn = get_db()
    by_dept = conn.execute('''SELECT COALESCE(d.department_name,'Unassigned') department_name,
                              COUNT(DISTINCT e.employee_id) employees,
                              COALESCE(SUM(p.gross_salary),0) gross,
                              COALESCE(SUM(p.total_deductions),0) deductions,
                              COALESCE(SUM(p.net_salary),0) net
                              FROM employees e LEFT JOIN departments d ON d.department_id=e.department_id
                              LEFT JOIN payroll p ON p.employee_id=e.employee_id
                              GROUP BY d.department_id ORDER BY gross DESC''').fetchall()
    conn.close()
    return render_template('reports.html', by_dept=by_dept)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
