-- SQLite
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary INTEGER,
    join_date TEXT
);

INSERT INTO employees (name, department, salary, join_date) VALUES
('Alice', 'Engineering', 120000, '2021-01-15'),
('Bob', 'Sales', 90000, '2022-03-20'),
('Charlie', 'Engineering', 110000, '2023-07-10');
