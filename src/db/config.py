from piccolo.engine import PostgresEngine


DB = PostgresEngine(
    config={
        "database": "hotei",
        "host": "localhost",
        "port": 5432,
        "user": "postgres",
        "password": "password"
    }
)
