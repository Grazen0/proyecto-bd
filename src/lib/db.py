import os
import re

from psycopg import Cursor, sql
from psycopg.rows import TupleRow

from lib.constants import SCHEMA


def select_schema(cur: Cursor):
    cur.execute(sql.SQL("SET SEARCH_PATH TO {}").format(sql.Literal(SCHEMA)))


def reset_schema(cur: Cursor):
    cur.execute(
        sql.SQL("DROP SCHEMA IF EXISTS {} CASCADE").format(sql.Identifier(SCHEMA))
    )
    cur.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(SCHEMA)))


def execute_file(cur: Cursor, path: str) -> Cursor[TupleRow]:
    print(f"Running {path}...")

    with open(path, "r") as file:
        return cur.execute(file.read())  # type: ignore


def load_table_csv(cur: Cursor, dir: str, filename: str):
    full_path = f"{dir}/{filename}"
    table_name = re.sub(r"(^\d+-|\.csv$)", "", filename)
    print(f"Loading {full_path} ({table_name})...")

    if (
        cur.execute(
            sql.SQL("SELECT 1 FROM {}").format(sql.Identifier(table_name))
        ).fetchone()
        != None
    ):
        print(f"Table {table_name} seems to be populated. Skipping...")
        return

    with open(full_path, "r") as file:
        header = file.readline().strip()
        column_names = header.split(",")

    cur.execute(
        sql.SQL("COPY {}({}) FROM {} DELIMITER ',' CSV HEADER ENCODING 'UTF8'").format(
            sql.Identifier(table_name),
            sql.SQL(", ").join(map(sql.Identifier, column_names)),
            sql.Literal(f"/{dir}/{filename}"),
        )
    )


def populate_from_dir(cur: Cursor, dir: str):
    files = os.listdir(dir)
    files.sort()
    for file in files:
        load_table_csv(cur, dir, file)
