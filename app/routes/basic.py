import uuid
from flask import render_template, request, session, redirect, Blueprint
from .utils import is_logged
from ..config import VERSION
from ..database import Database
from ..models import Session, Order, OrderTotal
from datetime import datetime

basic_blueprint = Blueprint('basic', __name__)

@basic_blueprint.route('/')
def index():
    """ Index page """
    return render_template(
        "index.html",
        title="Welcome",
        version=VERSION,
        logged=is_logged(),
    )

@basic_blueprint.route('/sessions/<session_id>', methods=["POST", "GET"])
def sessions_id(session_id:str):
    """ Single Session page """
    if not is_logged():
        return redirect(f"/login?session_id={session_id}")
    db = Database()
    if request.method == "POST":
        res = db.c.execute(
            'INSERT INTO user_session_order (user_id, session_id, order_number, order_name) VALUES (?, ?, ?, ?)',
            (
                session["user"]["id"],
                session_id,
                request.form["number"],
                request.form["name"]
            )
        )
        db.commit()
        if res:
            return redirect(f"/sessions/{session_id}")
    res_session = db.c.execute(
        'SELECT * FROM session WHERE id = ? LIMIT 1', (session_id,)
    ).fetchone()
    res_orders = db.c.execute(
        'SELECT * FROM user_session_order INNER JOIN user ON user.id = user_session_order.user_id WHERE session_id = ? ORDER by order_number ASC, name ASC', (session_id,)
    ).fetchall()
    res_orders_total = db.c.execute(
        'SELECT order_number, COUNT(user_id) FROM user_session_order WHERE session_id = ? GROUP BY order_number ORDER by order_number ASC', (session_id,)
    ).fetchall()
    current_session = Session(res_session)
    orders = [Order(row) for row in res_orders]
    orders_total = [OrderTotal(row) for row in res_orders_total]
    db.close()
    return render_template(
        "session.html",
        title=f"{current_session.title}",
        version=VERSION,
        logged=is_logged(),
        orders=orders,
        orders_total=orders_total,
        session=current_session,
    )

@basic_blueprint.route('/sessions', methods=["POST", "GET"])
def sessions():
    """ Sessions page """
    if not is_logged():
        return redirect("/login")
    db = Database()
    if request.method == "POST":
        new_session = str(uuid.uuid4())
        res = db.c.execute(
            'INSERT INTO session (id, date, title) VALUES (?, ?, ?)',
            (
                new_session,
                datetime.now().isoformat(),
                request.form["title"]
            )
        )
        db.commit()
        if res:
            return redirect(f"/sessions/{new_session}")
    res = db.c.execute(
        'SELECT * FROM session ORDER BY id DESC'
    ).fetchall()
    sessions = [Session(row) for row in res]
    db.close()
    return render_template(
        "sessions.html",
        title="Start eating!",
        version=VERSION,
        logged=is_logged(),
        sessions=sessions,
    )

@basic_blueprint.route("/login", methods=["POST", "GET"])
def login():
    """ Login page """
    output = ""
    if is_logged():
        return redirect("/")
    if request.method == "POST":
        db = Database()
        user_id = str(uuid.uuid4())
        res = db.c.execute(
            'INSERT INTO user (id, name) VALUES (?, ?)',
            (
                user_id,
                str(request.form["name"])
            )
        )
        db.commit()
        if res:
            session["user"] = {
                "id": user_id,
                "name": request.form["name"]
            }
            return redirect("/")
        else:
            output = ("error", "You bitch dont you try")
        db.close()
    return render_template(
        "login.html",
        output=output,
        version=VERSION,
        logged=False,
        title="Login",
    )

@basic_blueprint.route("/logout")
def logout():
    """ Logout page """
    session.pop("user", None)
    return redirect("/")
