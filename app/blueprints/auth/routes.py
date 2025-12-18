from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required

from ...extensions import db
from ...models import User, Group, Company, CompanyUser

bp = Blueprint("auth", __name__, template_folder="../../templates")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").lower().strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email, is_active=True).first()

        if not user or not user.check_password(password):
            flash("Invalid credentials", "error")
            return redirect(url_for("auth.login"))

        login_user(user)

        # 🔹 Bootstrap tenant (first login)
        membership = CompanyUser.query.filter_by(user_id=user.id, is_active=True).first()

        if not membership:
            group = Group(
                name=f"{user.full_name} Group",
                owner_user_id=user.id,
            )
            db.session.add(group)
            db.session.flush()

            company = Company(
                group_id=group.id,
                name=f"{user.full_name} Clinic",
            )
            db.session.add(company)
            db.session.flush()

            membership = CompanyUser(
                company_id=company.id,
                user_id=user.id,
                role="owner",
            )
            db.session.add(membership)

            db.session.commit()

        session["current_company_id"] = membership.company_id

        return redirect(url_for("agenda.today"))

    return render_template("auth/login.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("auth.login"))
