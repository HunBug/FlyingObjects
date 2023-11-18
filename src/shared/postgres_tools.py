from typing import Optional
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from .models import OrmBase


class PostgresTools:
    @staticmethod
    def get_default_config_dict() -> dict:
        return {
            "host": "postgres",
            "port": 5432,
            "database": "flying_simulator",
            "user": "postgres",
            "password": "postgres",
        }

    @staticmethod
    def get_db_url(config_dict: Optional[dict] = None) -> str:
        if config_dict is None:
            config_dict = PostgresTools.get_default_config_dict()

        database_uri = (
            "postgresql://"
            + f"{config_dict['user']}:{config_dict['password']}@"
            + f"{config_dict['host']}:{config_dict['port']}/"
            + f"{config_dict['database']}"
        )
        return database_uri

    @staticmethod
    def create_postgres_db(config_dict: Optional[dict] = None):
        if config_dict is None:
            config_dict = PostgresTools.get_default_config_dict()

        dbname = config_dict["database"]
        con = psycopg2.connect(
            dbname="postgres",
            user=config_dict["user"],
            password=config_dict["password"],
            host=config_dict["host"],
        )
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()

        # Create the database
        try:
            cur.execute(f"CREATE DATABASE {dbname}")
            print(f"Database {dbname} created successfully")
        except psycopg2.errors.DuplicateDatabase:
            print(f"Database {dbname} already exists")
        finally:
            cur.close()
            con.close()

    @staticmethod
    def create_tables(config_dict: Optional[dict] = None):
        if config_dict is None:
            config_dict = PostgresTools.get_default_config_dict()

        database_uri = PostgresTools.get_db_url(config_dict)
        engine = create_engine(database_uri)
        OrmBase.metadata.create_all(engine)
