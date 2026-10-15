# SQL Database Assistant MCP Server

A Python-based MCP server that imports employee data from a PDF into SQLite and allows AI applications to query the database using SQL.

## Features

- Import employee records from a PDF.
- Store employee data in SQLite.
- List available database tables.
- Run read-only SQL queries.
- Test tools using MCP Inspector.

## Tech Stack

- Python
- FastMCP
- SQLite
- pypdf
- uv
- MCP Inspector

## Project Structure

```text
sql-database-mcp/
├── main.py
├── README.md
├── company.db
├── pyproject.toml
├── uv.lock
└── pdfs/
    └── sql_database_mcp_sample_data.pdf
```

## Installation

Install the dependencies:

```powershell
uv sync
```

If needed, add the required packages:

```powershell
uv add fastmcp pypdf
```

## Run the MCP Server

```powershell
uv run fastmcp run main.py
```

## Run MCP Inspector

```powershell
uv run fastmcp dev inspector main.py
```

## Available MCP Tools

### 1. `import_pdf()`

Extracts employee records from the configured PDF and inserts or updates them in SQLite.

### 2. `list_tables()`

Lists tables available in the database.

### 3. `read_query(sql)`

Executes a read-only SQL SELECT query and returns the results.

## SQL Queries to Test

### Show all employees

```sql
SELECT * FROM employees
```

### Find IT employees

```sql
SELECT *
FROM employees
WHERE department = 'IT'
```

### Find employees in Bhopal

```sql
SELECT name, department, city
FROM employees
WHERE city = 'Bhopal'
```

### Find the three highest-paid employees

```sql
SELECT name, salary
FROM employees
ORDER BY salary DESC
LIMIT 3
```

### Count employees by department

```sql
SELECT department, COUNT(*) AS total_employees
FROM employees
GROUP BY department
```

### Calculate average salary by department

```sql
SELECT department, AVG(salary) AS average_salary
FROM employees
GROUP BY department
```

### Count all employees

```sql
SELECT COUNT(*) AS total_employees
FROM employees
```

### Find employees earning more than 50,000

```sql
SELECT name, salary
FROM employees
WHERE salary > 50000
ORDER BY salary DESC
```

## Troubleshooting

### Employee table has no `employee_id` column

The existing database may have an older table schema. Stop the server, back up important data, and delete `company.db` if you can safely reset it. Restart the server and call `import_pdf()` again.

### PDF not found

Confirm that the PDF exists at:

```text
pdfs/sql_database_mcp_sample_data.pdf
```

## Security

The query tool is intended for read-only SELECT statements. Add stronger query validation, timeouts, and access controls before using this server in production.

## Documentation

- [FastMCP](https://gofastmcp.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [SQLite](https://www.sqlite.org/docs.html)
- [pypdf](https://pypdf.readthedocs.io/)
- [uv](https://docs.astral.sh/uv/)
