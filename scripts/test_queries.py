import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
db_path = os.path.join(BASE_DIR, "autoservice.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("--- Testing Tables in Database ---")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
tables = [row[0] for row in cursor.fetchall()]
print("Tables count:", len(tables), "->", tables)

for t in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {t};")
    count = cursor.fetchone()[0]
    print(f"  {t}: {count} records")

print("\n--- Testing Teacher's Special Query (NO JOINs) ---")
teacher_query = """
SELECT 
    cl.id AS client_id,
    cl.full_name AS client_name,
    cl.phone AS client_phone,
    c.brand || ' ' || c.model AS car_model,
    c.license_plate,
    wo.order_number,
    wo.created_at AS order_date,
    s.name AS service_name,
    os.unit_price * os.quantity AS service_cost
FROM 
    clients cl,
    cars c,
    work_orders wo,
    order_services os,
    services s
WHERE 
    cl.id = c.client_id
    AND c.id = wo.car_id
    AND wo.id = os.work_order_id
    AND os.service_id = s.id
ORDER BY 
    cl.id, wo.created_at;
"""

cursor.execute(teacher_query)
results = cursor.fetchall()
print(f"Results returned: {len(results)} rows")
for row in results[:5]:
    print(" ", row)

print("\n--- Verifying all 12 queries from queries.sql ---")
with open(os.path.join(BASE_DIR, "queries.sql"), "r", encoding="utf-8") as f:
    sql_text = f.read()

# Split queries by semicolon
queries = [q.strip() for q in sql_text.split(";") if q.strip()]
valid_queries = 0
for idx, q in enumerate(queries, 1):
    # filter out comment-only chunks
    lines = [l for l in q.splitlines() if not l.strip().startswith("--") and l.strip()]
    if not lines:
        continue
    clean_sql = "\n".join(lines)
    try:
        cursor.execute(clean_sql)
        res = cursor.fetchall()
        print(f"Query #{idx} executed successfully: {len(res)} rows returned")
        valid_queries += 1
    except Exception as e:
        print(f"Query #{idx} failed: {e}")

print(f"\nTotal queries verified: {valid_queries}")
conn.close()
