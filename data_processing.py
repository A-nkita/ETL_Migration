import mysql.connector as ms
import pyodbc
import json
import sys
from logger_config import setup_logger

# Setup logger
logger = setup_logger(log_file="data_migration.log", log_level="INFO")


def load_config(env):
    config_file = f"config/{env}.configs.json"
    try:
        with open(config_file, "r") as file:
            config = json.load(file)
        logger.info("Loaded config: %s", tuple(config.values()))
        return config
    except Exception as e:
        logger.error("Error loading config: %s", e)
        sys.exit(1)


def db_connect_mysql(host, user, password, database, port):
    try:
        conn = ms.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        logger.info("Connected to MySQL successfully.")
        return conn.cursor(dictionary=True), conn
    except ms.Error as e:
        logger.error("Error connecting to MySQL: %s", e)
        sys.exit(1)


def db_connect_mssql(server, database, user=None, password=None, trusted_connection=False):
    try:
        if trusted_connection:
            conn = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"Trusted_Connection=yes;"
            )
        else:
            conn = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"UID={user};"
                f"PWD={password};"
            )
        logger.info("Connected to MSSQL successfully.")
        return conn.cursor(), conn
    except Exception as e:
        logger.error("Error connecting to MSSQL: %s", e)
        sys.exit(1)


def db_data_dump(mysql_cur, mssql_cur, mysql_table, mssql_table):
    try:
        mysql_cur.execute(f"SELECT * FROM {mysql_table}")
        rows = mysql_cur.fetchall()

        if not rows:
            logger.warning(f"No data found in MySQL table '{mysql_table}'.")
            return

        columns = rows[0].keys()
        insert_query = f"INSERT INTO {mssql_table} ({', '.join(columns)}) VALUES ({', '.join(['?' for _ in columns])})"

        logger.info("Insert query: %s", insert_query)

        mssql_cur.execute(f"SET IDENTITY_INSERT {mssql_table} ON")
        for row in rows:
            mssql_cur.execute(insert_query, tuple(row.values()))
        mssql_cur.execute(f"SET IDENTITY_INSERT {mssql_table} OFF")

        logger.info(f"Successfully inserted {len(rows)} rows into MSSQL table '{mssql_table}'.")
    except Exception as e:
        logger.error("Error during data migration: %s", e)
        sys.exit(1)


def main():
    env = input("Enter Environment: ").strip().lower()
    config = load_config(env)

    mysql_cur, mysql_conn = db_connect_mysql(
        config["mysql_host"],
        config["mysql_user"],
        config["mysql_password"],
        config["mysql_database"],
        config["mysql_port"]
    )
    mssql_cur, mssql_conn = db_connect_mssql(
        config["mssql_host"],
        config["mssql_database"],
        config.get("mssql_user"),
        config.get("mssql_password"),
        config.get("trusted_connection", False)
    )

    db_data_dump(mysql_cur, mssql_cur, config.get("mysql_table", "Data_Migration"),
                 config.get("mssql_table", "Data_Migration"))

    mssql_conn.commit()
    mysql_cur.close()
    mysql_conn.close()
    mssql_cur.close()
    mssql_conn.close()
    logger.info("Data migration completed successfully!")


if __name__ == "__main__":
    main()
