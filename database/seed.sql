INSERT INTO departments(department_name) VALUES ('Human Resources'),('Finance'),('Information Technology'),('Marketing');
INSERT INTO employees(employee_code,first_name,last_name,email,phone,department_id,designation,joining_date,basic_salary,status)
VALUES
('EMP001','Rupesh','Yallamgari','rupesh@example.com','9876543210',3,'Software Developer','2026-10-01',50000,'Active'),
('EMP002','Rahul','Kumar','rahul@example.com','9876501234',2,'Accountant','2026-08-15',45000,'Active'),
('EMP003','Ananya','Reddy','ananya@example.com','9876512345',1,'HR Executive','2026-07-10',42000,'Active');
INSERT INTO payroll(employee_id,pay_month,basic_salary,hra,allowance,bonus,gross_salary,pf,esi,professional_tax,tds,total_deductions,net_salary,status)
VALUES (1,'2026-10',50000,20000,3000,2000,75000,9000,562.5,200,0,9762.5,65237.5,'Processed'),
(2,'2026-10',45000,18000,2000,0,65000,7800,487.5,200,0,8487.5,56512.5,'Processed');
