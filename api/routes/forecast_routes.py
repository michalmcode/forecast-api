from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from api.schemas import TrendForecastSchema
from api.services import trend_method

bp = Blueprint("forecast", __name__, url_prefix="/forecast")


@bp.route("/trend", methods=["POST"])
def create_trend_forecast():
    data = request.get_json()

    # Input validation
    try:
        validated_data = TrendForecastSchema().load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    result = trend_method.calculate(validated_data)

    return jsonify(result)
