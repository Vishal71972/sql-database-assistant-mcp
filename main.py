import re

import sqlite3
from pathlib import Path
from fastmcp import FastMCP
from pypdf import PdfReader
# create server
mcp = FastMCP("SQL Database Assistant")

#database path define 
#currnet folder ke parent folder ke company.db file
DB_PATH = Path(__file__).parent / "company.db"
PDF_PATH =  Path(__file__).parent / "pdfs" / "sql_database_mcp_sample_data.pdf"



#database connection
def get_connection():
    return sqlite3.connect(DB_PATH)


#database initilization
def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                employee_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                salary REAL NOT NULL,
                city TEXT NOT NULL
            )
        """)


@mcp.tool()
def import_pdf() -> str:
    """Import employee records from the sample PDF into SQLite."""
    if not PDF_PATH.exists():
        raise FileNotFoundError(
            f"PDF not found: {PDF_PATH}"
        )

    reader = PdfReader(str(PDF_PATH))
    text = "\n".join(
        page.extract_text() or "" for page in reader.pages
    )

    pattern = re.compile(
        r"(?m)^\s*(\d{3})\s+"
        r"([A-Za-z ]+?)\s+"
        r"(IT|HR|Finance|Sales)\s+"
        r"(\d{5,6})\s+"
        r"(Bhopal|Indore|Patna|Delhi)\s*$"
    )

    records = pattern.findall(text)

    if not records:
        return (
            "No employee records were detected. "
            "Check the PDF text format."
        )

    with get_connection() as conn:
        conn.executemany("""
            INSERT INTO employees
                (employee_id, name, department, salary, city)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(employee_id) DO UPDATE SET
                name = excluded.name,
                department = excluded.department,
                salary = excluded.salary,
                city = excluded.city
        """, [
            (int(emp_id), name.strip(), department,
             float(salary), city)
            for emp_id, name, department, salary, city in records
        ])

    return f"Imported or updated {len(records)} employee records."


@mcp.tool()
def list_tables() -> list[str]:
    """List tables in the database."""
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """).fetchall()

    return [row[0] for row in rows]


@mcp.tool()
def read_query(sql: str) -> list[dict]:
    """Execute a read-only SELECT query."""
    query = sql.strip()

    if not re.match(r"(?is)^SELECT\b", query):
        raise ValueError("Only SELECT queries are allowed.")

    if ";" in query:
        raise ValueError("Only one SQL statement is allowed.")

    with get_connection() as conn:
        conn.execute("PRAGMA query_only = ON")
        conn.row_factory = sqlite3.Row
        rows = conn.execute(query).fetchall()
        return [dict(row) for row in rows]

# call database
initialize_database()

#start server
if __name__ == "__main__":
    mcp.run()


