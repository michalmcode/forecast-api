from marshmallow import fields

from api import ma


class TrendForecastSchema(ma.Schema):
    values = fields.List(fields.Float(), required=True)
    periods = fields.Int(required=True)
