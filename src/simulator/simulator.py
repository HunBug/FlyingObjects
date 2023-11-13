from datetime import datetime, timedelta
from generator import Generator
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    logging.info("Initializing the simulation")
    generator = Generator(start_time=datetime.now(),
                            simulation_duration=timedelta(seconds=3),
                            simulation_resolution=timedelta(milliseconds=150),
                            num_objects=5)
    logging.info("Running the simulation")
    generator.run_simulation()
    logging.info("Simulation finished")