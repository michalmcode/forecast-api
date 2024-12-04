from botocore.exceptions import ClientError
from flask import Blueprint, send_file, Response, jsonify

from api.utils import aws_storage

bp = Blueprint("file", __name__, url_prefix="/file")


@bp.route("/download/<filename>", methods=["GET"])
def get_file(filename: str) -> Response:
    try:
        data = aws_storage.download_file(filename)
        return send_file(
            data,
            as_attachment=True,
            mimetype="image/png",
            download_name="forecast_plot.png",
        )
    except ClientError as err:
        return jsonify({"error": str(err)}), 500
