# Employee Payroll & Statutory Deduction Management System

A college-ready web application for employee records, payroll generation and statutory deductions. Built with **Python Flask + SQLite + HTML/CSS/JavaScript**.

## Features
- Dashboard with employee/payroll/deduction totals
- Employee CRUD: add and delete employees
- Payroll generation using basic salary + HRA + allowances + bonus
- Statutory deductions: PF, ESI, Professional Tax and TDS
- Automatic gross salary, total deductions and net salary calculation
- Department-wise payroll report
- SQLite database included; no XAMPP/MySQL is required for the demo

## Run in VS Code
1. Extract the ZIP.
2. Open the extracted `Employee_Payroll_Statutory_Deduction` folder in VS Code.
3. Open Terminal: **Terminal > New Terminal**.
4. Create a virtual environment (optional but recommended):
   - Windows: `py -m venv .venv`
   - Activate: `.venv\\Scripts\\activate`
5. Install Flask: `pip install -r requirements.txt`
6. Run: `python app.py`
7. Open Chrome: `http://127.0.0.1:5000/`

## Presentation demo
1. Dashboard
2. Employees -> add a new employee
3. Payroll -> select employee and generate salary
4. Statutory Deductions -> show PF, ESI, PT and TDS
5. Reports -> show department-wise totals

## Formula used for demo
Gross = Basic + HRA + Allowance + Bonus
PF = Gross x PF rate / 100 (default 12%)
ESI = Gross x ESI rate / 100 (default 0.75%)
Total deductions = PF + ESI + PT + TDS
Net salary = Gross - Total deductions

> The statutory rates in this academic demo are configurable inputs and should not be treated as legal/payroll advice. Verify applicable rates and wage ceilings before real-world use.
