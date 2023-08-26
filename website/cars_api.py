from flask import Blueprint
from .database import Database

db = Database()

bp = Blueprint("car-api", __name__, url_prefix="/api/cars")
