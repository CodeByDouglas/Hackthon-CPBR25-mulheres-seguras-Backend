from flask import Blueprint

bp = Blueprint("users", __name__)


@bp.route("/ping")
def ping():
    return "pong-users"
