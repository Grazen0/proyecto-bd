import psycopg

from lib.db import execute_file, populate_from_dir, reset_schema, select_schema

with psycopg.connect() as conn:
    with conn.cursor() as cur:
        reset_schema(cur)
        select_schema(cur)

        execute_file(cur, "sql/init.sql")
        populate_from_dir(cur, "data/manual")

    conn.commit()
