import logging
from datetime import datetime, timedelta
from multiprocessing import Process

from .generator import Generator
from .sql_data_writer import SqlDataWriter

logging.basicConfig(level=logging.INFO)


def run_single_simulation(
    database_uri, start_time, duration, resolution, num_objects, simulation_id
):
    writer = SqlDataWriter(database_uri, simulation_id=simulation_id)
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
    simulation_start_time = datetime.now()
    simulation_duration = timedelta(hours=10)
    simulation_resolution = timedelta(milliseconds=150)
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

    writer = SqlDataWriter(database_uri)
    writer.connect()
    simulation_id = writer.log_simulation_start(datetime.now())
    writer.close()
    if len(process_num_objects) == 1:
        logging.info("Running single process simulation")
        run_single_simulation(
            database_uri,
            simulation_start_time,
            simulation_duration,
            simulation_resolution,
            process_num_objects[0],
            simulation_id,
        )
    else:
        logging.info("Running multi process simulation")
        # Create and start processes
        processes = []
        for num_objects in process_num_objects:
            p = Process(
                target=run_single_simulation,
                args=(
                    database_uri,
                    simulation_start_time,
                    simulation_duration,
                    simulation_resolution,
                    num_objects,
                    simulation_id,
                ),
            )
            p.start()
            processes.append(p)

        # Wait for all processes to complete
        for p in processes:
            p.join()

    logging.info("All simulations finished")
    writer = SqlDataWriter(database_uri, simulation_id=simulation_id)
    writer.connect()
    writer.log_simulation_end(datetime.now())
    writer.close()


if __name__ == "__main__":
    main()
