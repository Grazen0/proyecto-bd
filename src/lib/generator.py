import csv
from typing import Any, Callable

from lib.constants import FACTOR, GENERATED_DIR


class EpicDataGenerator:
    current_index = 0

    def generate(
        self,
        n: int,
        table_name: str,
        spec: dict[str, Callable[[int], Any]],
        n_strict: bool = False,
    ):
        if n_strict:
            n_real = n
        else:
            n_real = n * FACTOR
        results = []

        columns = spec.keys()

        filename = f"{self.current_index:02}-{table_name}.csv"
        print(f"Generating {n_real} rows for {filename}...")

        with open(f"{GENERATED_DIR}/{filename}", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(columns)
            for i in range(n_real):
                tup = {col: spec[col](i) for col in columns}
                writer.writerow([tup[col] for col in columns])
                results.append(tup)

        self.current_index += 1
        return results
