import os
import psycopg2
from faker import Faker
from dotenv import load_dotenv

load_dotenv()


DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT", "5432"),
    "host": os.getenv("DB_HOST", "localhost"),
}


def populate(n_clients):
    fake = Faker("pt_BR")
    conn = psycopg2.connect(**DB_CONFIG)

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS clientes (
                        id SERIAL PRIMARY KEY,
                        nome VARCHAR(100) NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL
                    )
                    """
                )
                for _ in range(n_clients):
                    nome = fake.name()
                    email = fake.unique.email()
                    cur.execute(
                        """
                        INSERT INTO clientes (nome, email)
                        VALUES (%s, %s)
                        """,
                        (nome, email),
                    )
        print(f"{n_clients} clientes inseridos com sucesso!")
    finally:
        conn.close()


if __name__ == "__main__":
    TOTAL = 10000  # 10.000
    populate(TOTAL)
