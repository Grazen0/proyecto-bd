import psycopg

from lib.constants import GENERATED_DIR
from lib.db import populate_from_dir, select_schema

with psycopg.connect() as conn:
    with conn.cursor() as cur:
        select_schema(cur)
        populate_from_dir(cur, GENERATED_DIR)

    conn.commit()
