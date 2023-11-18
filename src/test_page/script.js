function startSimulation() {
    fetch('http://127.0.0.1:6002/start_simulation', {
            method: 'POST',
            headers: {
                accept: 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
}

function queryObjectTrajectory() {
    const objectId = document.getElementById('object_id').value;
    const startTime = document.getElementById('start_time_obj').value;
    const endTime = document.getElementById('end_time_obj').value;
    
    fetch(`http://127.0.0.1:6001/query_object_trajectory?object_id=${objectId}&start_time=${startTime}&end_time=${endTime}`, {
            method: 'GET',
            headers: {
                accept: 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
}

function querySectorSnapshot() {
    const sectorId = document.getElementById('sector_id').value;
    const startTime = document.getElementById('start_time_sector').value;
    const endTime = document.getElementById('end_time_sector').value;

    fetch(`http://127.0.0.1:6001/query_sector_snapshot?sector_id=${sectorId}&start_time=${startTime}&end_time=${endTime}`, {
            method: 'GET',
            headers: {
                accept: 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
}
