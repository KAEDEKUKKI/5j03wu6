from flask import Blueprint

group_bp = Blueprint('group', __name__)

from . import view
from . import models
