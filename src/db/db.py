import psycopg2
from config import DB_CONFIG


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def test_connection():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print(f"Connected to :{version}")
    cur.close()
    conn.close()


if __name__ == "__main__":
    test_connection()
