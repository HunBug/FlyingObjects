# Flying Objects Simulation

## Overview
This project simulates the flight of 500 objects within a defined 2D world, implemented entirely in Python. It includes a generator for simulating flying objects, a Flask application for querying simulation data, PostgreSQL for data storage, and additional tools for testing and visualization.

### Key Components
- **Generator Application**: Simulates 500 independent flying objects, running on separate processes to bypass the Python GIL.
- **REST API app**: Provides endpoints for querying simulation data, returning results in JSON format.
- **PostgreSQL**: Used for persisting simulation data.
- **Additional Tools**: Includes a Jupyter Notebook for bezier curve visualization and a basic HTML page for REST API testing.

## Running the Project
To run the demo of this project, follow these steps:

1. **Clone the Repository**:
```
git clone https://github.com/HunBug/FlyingObjects
```
2. **Create a Directory for PostgreSQL Data**:
Navigate to the repo root folder and create a folder for PostgreSQL data:
```
mkdir postgres-data
```
3. **Build Docker Image**:
```
docker compose build
```
![Docker Build](/docs/images/docker_build.png)

4. **Run Docker Containers**:    
```
docker compose up
```
![Docker Up](/docs/images/docker_up.png)

5. **Testing** *(more information in the next section)*: 
- Use the simple HTML page located in the `/src/test_page` folder.
- Alternatively, use an application like Postman to interact with the API.

### Important Note on Port Usage

The `docker-compose.yml` file specifies certain ports to be opened on the host machine. Ensure these ports are free or edit the `docker-compose.yml` file to use different ports. By default, the following ports are used:

- **6432**: PostgreSQL server.
- **6002**: Simulator REST API.
- **6001**: Query REST API.

If these ports are already in use on your system, you will need to modify the `docker-compose.yml` file to specify alternative ports before running `docker compose up`.

## Testing the Flying Objects Simulation

The simulation project offers three REST API endpoints, accessible once all Docker containers are up and running. You can test these endpoints using the provided basic HTML page or with a tool like Postman.

### Starting the Simulation
- **Endpoint**: `http://127.0.0.1:6002/start_simulation`
- **Method**: POST
- **Note**: Be cautious to trigger this endpoint only once at a time, as the system currently does not check for already running simulations. To confirm the simulation has started and track its progress, monitor the Docker logs. On an 8-thread processor, the simulation takes approximately 15-20 minutes to complete.

![Docker Logs](/docs/images/sim_finished.png)

#### Using Basic HTML Page
- Open the HTML page located in `/src/test_page`.
- Click the button designed to start the simulation.
- Observe the logs or Docker output to monitor the simulation progress.

#### Using Postman
- Open Postman and create a new request.
- Set the request type to `POST`.
- Enter the URL: `http://127.0.0.1:6002/start_simulation`.
- Send the request and monitor the Docker logs for progress.

### Querying the Simulation Data
After the simulation completes, use the following endpoints to query the data. Note that you will need `Object_ID`s, which are randomly generated during the simulation.

#### Obtaining Object_IDs
- **From Docker Logs**: 
  - You can find `Object_ID`s in the Docker log output of the simulator. These IDs are necessary for querying specific object trajectories.
- **Direct Database Access**:
  - Alternatively, connect directly to the PostgreSQL database to fetch `Object_ID`s. Use the following database credentials:
    - **Host**: `127.0.0.1`
    - **Port**: `6432`
    - **Database**: `flying_simulator`
    - **User**: `postgres`
    - **Password**: `postgres`
  - You can use a database tool like PGAdmin or a similar SQL client to connect and query the `Object_ID`s.

#### Simulation Timeframe
- The simulation uses the current time of the host machine as the "start date" for each simulation run. Keep this in mind when querying data, as you'll need to align your query's timeframe with the simulation's timeframe.

#### API Endpoints for Querying Data

1. **Query Object Trajectory**
   - **Endpoint**: `http://127.0.0.1:6001/query_object_trajectory`
   - **Parameters**: `object_id`, `start_time`, `end_time`
   - **Method**: GET

2. **Query Sector Snapshot**
   - **Endpoint**: `http://127.0.0.1:6001/query_sector_snapshot`
   - **Parameters**: `sector_id`, `start_time`, `end_time`
   - **Method**: GET

#### Using Basic HTML Page
- Open the HTML test page.
- Fill in the required parameters for the query you wish to execute.
- Click the corresponding button to send the query.
- Currently, the results will be logged to the console. Check the browser's developer console to view the output.

![HTML Page](/docs/images/test_query.png)

#### Using Postman
- Open Postman and create a new request.
- Set the request type to `GET`.
- Enter the URL with appropriate query parameters. For example:
  - For object trajectory: `http://127.0.0.1:6001/query_object_trajectory?object_id=<ID>&start_time=<START_TIME>&end_time=<END_TIME>`
  - For sector snapshot: `http://127.0.0.1:6001/query_sector_snapshot?sector_id=<SECTOR_ID>&start_time=<START_TIME>&end_time=<END_TIME>`
- Send the request and view the results in Postman.

## Debugging and Visualization
- **Jupyter Notebook**: Use the provided notebook to visualize bezier curves.
- **Test HTML page**: Test the Flask API endpoints with the provided HTML page or tools like Postman.

## Future Development

### Improvements on the test page
- The current setup lacks user-friendly feedback mechanisms for API responses. This can be improved in future versions.
- Consider implementing checks to prevent multiple simultaneous simulations and to provide clearer feedback on the status of the simulation.
- Enhancing the HTML test page to display results directly on the page, rather than in the console, is planned for future updates.
- Additional user convenience features, like querying specific object IDs or handling multiple simulation runs.

### Improvements on implementation
- **Add Unit Tests**: Implement unit tests for angle normalization, regular expressions, bezier path calculations, etc.
- **Random-Init Seed**: Introduce a seed for random initialization to allow reproducibility of simulations.
- **Address TODOs**: Complete all TODO items currently in the code.
- **Code Style Consistency**: Ensure consistent coding style across the entire project.
- **Config Management**: Read database and other configurations from environment variables or a configuration file.
- **Memory Considerations**: Current implementation assumes that queried data fits into memory. Pagination is not yet implemented.


