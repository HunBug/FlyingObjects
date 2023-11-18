from datetime import datetime
from itertools import groupby
from operator import attrgetter

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from shared.models import FlyingObjectOrm, FlyingObjectStateOrm

app = Flask(__name__)

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
app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
db = SQLAlchemy(app)


@app.route("/query_object_trajectory", methods=["GET"])
def query_object_trajectory():
    object_id = request.args.get("object_id")
    start_time = datetime.fromisoformat(request.args.get("start_time"))
    end_time = datetime.fromisoformat(request.args.get("end_time"))

    path_result = (
        db.session.query(FlyingObjectStateOrm)
        .filter(
            FlyingObjectStateOrm.object_id == object_id,
            FlyingObjectStateOrm.state_time >= start_time,
            FlyingObjectStateOrm.state_time <= end_time,
        )
        .all()
    )
    flying_object = (
        db.session.query(FlyingObjectOrm)
        .filter(FlyingObjectOrm.object_id == object_id)
        .first()
    )

    result = {
        "object_id": flying_object.object_id,
        "payload": flying_object.payload,
        "speed": flying_object.speed,
        "created_time": flying_object.created_time,
        "path": [
            {
                "x": state.x,
                "y": state.y,
                "angle": state.angle,
                "state_time": state.state_time,
                "expire_time": state.expire_time,
                "sector": state.sector,
            }
            for state in path_result
        ],
    }

    return jsonify(result)


@app.route("/query_sector_snapshot", methods=["GET"])
def query_sector_snapshot():
    sector_id = request.args.get("sector_id")
    start_time = datetime.fromisoformat(request.args.get("start_time"))
    end_time = datetime.fromisoformat(request.args.get("end_time"))

    objects_result = (
        db.session.query(FlyingObjectStateOrm)
        .filter(
            FlyingObjectStateOrm.sector == sector_id,
            FlyingObjectStateOrm.state_time >= start_time,
            FlyingObjectStateOrm.state_time <= end_time,
        )
        .order_by(FlyingObjectStateOrm.object_id, FlyingObjectStateOrm.state_time)
        .all()
    )

    # result = {
    #     "sector_id": sector_id,
    #     "start_time": start_time,
    #     "end_time": end_time,
    #     "objects": [{
    #         "object_id": state.object_id,
    #         "x": state.x,
    #         "y": state.y,
    #         "angle": state.angle,
    #         "state_time": state.state_time,
    #         "expire_time": state.expire_time,
    #         "sector": state.sector
    #     } for state in objects_result]
    # }

    # Group the results by object_id
    grouped_results = groupby(objects_result, key=attrgetter("object_id"))

    # Format the results
    result = {
        "sector_id": sector_id,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "objects": [
            {
                "object_id": object_id,
                "states": [
                    {
                        "x": state.x,
                        "y": state.y,
                        "angle": state.angle,
                        "state_time": state.state_time.isoformat(),
                        "expire_time": state.expire_time,
                        "sector": state.sector,
                    }
                    for state in states
                ],
            }
            for object_id, states in grouped_results
        ],
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
