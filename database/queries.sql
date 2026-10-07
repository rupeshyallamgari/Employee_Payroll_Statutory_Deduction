-- Active employees
SELECT * FROM employees WHERE status='Active';
-- Payroll with employee names
SELECT e.employee_code, e.first_name, e.last_name, p.pay_month, p.gross_salary, p.total_deductions, p.net_salary
FROM payroll p JOIN employees e ON e.employee_id=p.employee_id;
-- Statutory totals
SELECT SUM(pf) AS PF, SUM(esi) AS ESI, SUM(professional_tax) AS Professional_Tax, SUM(tds) AS TDS, SUM(total_deductions) AS Total
FROM payroll;
