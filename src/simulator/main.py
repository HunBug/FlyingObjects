import argparse
import asyncio
import logging
from datetime import datetime, timedelta
from multiprocessing import Process
from threading import Thread

from flask import Flask, jsonify
from flask_cors import CORS

from shared.postgres_tools import PostgresTools

from .generator import Generator
from .sql_data_writer import SqlDataWriter

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
CORS(app)


def simulation_task(
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


async def run_simulation():
    logging.basicConfig(level=logging.INFO)

    logging.info("Initializing the database")
    database_config = PostgresTools.get_default_config_dict()  # read from config file
    PostgresTools.create_postgres_db(database_config)
    PostgresTools.create_tables(database_config)

    database_uri = PostgresTools.get_db_url(database_config)

    logging.info("Initializing the simulation")

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
        simulation_task(
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
                target=simulation_task,
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


@app.route("/start_simulation", methods=["POST"])
def start_simulation():
    thread = Thread(target=lambda: asyncio.run(run_simulation()))
    thread.start()
    return jsonify({"message": "Simulation started"})


def main():
    parser = argparse.ArgumentParser(description="Run the flying simulator.")
    parser.add_argument("--api", action="store_true", help="Run as a REST API server")
    args = parser.parse_args()

    if args.api:
        app.run(host="0.0.0.0", debug=True, port=5000)
    else:
        asyncio.run(run_simulation())


if __name__ == "__main__":
    main()
