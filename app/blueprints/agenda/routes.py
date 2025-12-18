from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint("agenda", __name__, template_folder="../../templates")


@bp.route("/today")
@login_required
def today():
    return render_template("agenda/today.html")
