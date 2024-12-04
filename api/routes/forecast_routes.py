from flask import Blueprint, jsonify, request, Response
from marshmallow import ValidationError

from api.schemas import TrendForecastSchema, MovingAverageForecastSchema
from api.services import trend_method, moving_avg_method

bp = Blueprint("forecast", __name__, url_prefix="/forecast")


@bp.route("/trend", methods=["POST"])
def create_trend_forecast() -> Response | tuple:
    data = request.get_json()

    # Input validation
    try:
        validated_data = TrendForecastSchema().load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    result, plot_filename = trend_method.calculate(validated_data)
    plot_url = (
        f"{request.url_root}file/download/{plot_filename}" if plot_filename else ""
    )

    return jsonify({"result": result, "plot": plot_url})


@bp.route("/moving-average", methods=["POST"])
def create_move_average_forecast() -> Response | tuple:
    data = request.get_json()

    # Input validation
    try:
        validated_data = MovingAverageForecastSchema().load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    result = moving_avg_method.calculate(validated_data)

    return jsonify({"result": result})
