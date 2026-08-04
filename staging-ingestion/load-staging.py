import os
import psycopg2
from urllib.parse import urlparse


def _load_env_file():
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if not os.path.exists(env_path):
        return

    with open(env_path, "r", encoding="utf-8") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env_file()


def load_csvs_to_staging():
    conn_str = os.getenv("POSTGRES_CONNECTION")
    if not conn_str:
        raise RuntimeError("POSTGRES_CONNECTION is not set in the environment or .env file")

    parsed = urlparse(conn_str)
    conn = psycopg2.connect(
        host=parsed.hostname,
        port=parsed.port,
        dbname=parsed.path.lstrip("/"),
        user=parsed.username,
        password=parsed.password,
        sslmode="require",
    )
    conn.autocommit = True

    base_dir = os.path.join(os.path.dirname(__file__), "data", "dataset")
    files = [
        ("staging.customers", "customers.csv"),
        ("staging.stores", "stores.csv"),
        ("staging.products", "products.csv"),
        ("staging.employees", "employees.csv"),
        ("staging.orders", "orders.csv"),
        ("staging.order_items", "order_items.csv"),
    ]

    try:
        with conn.cursor() as cur:
            for table_name, filename in files:
                cur.execute(f"TRUNCATE TABLE {table_name}")
                path = os.path.join(base_dir, filename)
                with open(path, "r", encoding="utf-8", newline="") as csv_file:
                    cur.copy_expert(
                        f"COPY {table_name} FROM STDIN WITH (FORMAT csv, HEADER true)",
                        csv_file,
                    )
                print(f"Loaded {filename} -> {table_name}")
    finally:
        conn.close()


def main():
    load_csvs_to_staging()


if __name__ == "__main__":
    main()
