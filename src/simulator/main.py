from datetime import datetime, timedelta
from .generator import Generator
from .sql_data_writer import SqlDataWriter
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    logging.info("Initializing the simulation")

    database_config = {
        "host": "localhost",
        "port": 5432,
        "database": "flying_simulator",
        "user": "postgres",
        "password": "postgres",
    }
    database_uri = "postgresql://" +\
                    f"{database_config['user']}:{database_config['password']}@" +\
                    f"{database_config['host']}:{database_config['port']}/" +\
                    f"{database_config['database']}"
    writer = SqlDataWriter(database_uri)
    writer.connect()
    
    generator = Generator(start_time=datetime.now(),
                            simulation_duration=timedelta(hours=10),
                            simulation_resolution=timedelta(milliseconds=150),
                            num_objects=10,
                            data_writer=writer)
    logging.info("Running the simulation")
    generator.run_simulation()
    logging.info("Simulation finished")
    writer.close()