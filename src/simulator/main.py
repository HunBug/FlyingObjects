import logging
from datetime import datetime, timedelta
from multiprocessing import Process

from .generator import Generator
from .sql_data_writer import SqlDataWriter

logging.basicConfig(level=logging.INFO)


def run_single_simulation(database_uri, start_time, duration, resolution, num_objects):
    writer = SqlDataWriter(database_uri)
    writer.connect()

    generator = Generator(
        start_time=start_time,
        simulation_duration=duration,
        simulation_resolution=resolution,
        num_objects=num_objects,
        data_writer=writer,
    )

    generator.run_simulation()
    writer.close()


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Initializing the simulation")

    database_config = {
        "host": "localhost",
        "port": 5432,
        "database": "flying_simulator",
        "user": "postgres",
        "password": "postgres",
    }
    database_uri = (
        "postgresql://"
        + f"{database_config['user']}:{database_config['password']}@"
        + f"{database_config['host']}:{database_config['port']}/"
        + f"{database_config['database']}"
    )

    # Define your simulation parameters
    start_time = datetime.now()
    duration = timedelta(hours=10)
    resolution = timedelta(milliseconds=150)
    process_num_objects = [
        62,
        62,
        62,
        62,
        62,
        62,
        62,
        66,
    ]  # Number of objects to generate per process

    if len(process_num_objects) == 1:
        logging.info("Running single process simulation")
        run_single_simulation(
            database_uri, start_time, duration, resolution, process_num_objects[0]
        )
    else:
        logging.info("Running multi process simulation")
        # Create and start processes
        processes = []
        for num_objects in process_num_objects:
            p = Process(
                target=run_single_simulation,
                args=(database_uri, start_time, duration, resolution, num_objects),
            )
            p.start()
            processes.append(p)

        # Wait for all processes to complete
        for p in processes:
            p.join()

    logging.info("All simulations finished")


if __name__ == "__main__":
    main()
