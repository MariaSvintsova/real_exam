"""
This is a Flask application that provides an API for managing friends' dates of birthday.

Dependencies:
- marshmallow
- Flask
- flask_sqlalchemy


Endpoints:
- GET /birthday/ : Retrieves all birthdays
- GET /birthday/<friend_id> : Retrieves birthday of specific person by ID
- POST /birthday : Creates a new date
- PUT /birthday/<friend_id> : Updates an existing date
- DELETE /birthday/<friend_id> : Deletes a birthday.

Models:
- Birthday : Represents a birthday in the database

Schemas:
- BirthdaySchema : Schema for serializing/deserializing Birthday objects

"""
from datetime import datetime

from marshmallow import Schema, fields
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config.from_pyfile("config.py")
app.config.from_envvar("APP_SETTINGS", silent=True)

db = SQLAlchemy(app)


class Birthday(db.Model):
    """
    Represents a friend's birthday in the database.

    Attributes:
        tablename (str): The name of the database table.
        friend_id (int): The ID of the friend (primary key).
        fio (str): The full name of the friend.
        date (date): The date of the birthday.
        wish (str): Variants of presents.
    """
    __tablename__ = 'birthday'
    friend_id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(300))
    date = db.Column(db.Date)
    wish = db.Column(db.String(255))


class BirthdaySchema(Schema):
    """
    Schema for serializing/deserializing Birthday objects.
    """
    friend_id = fields.Integer(dump_only=True)
    fio = fields.String()
    date = fields.Date()
    wish = fields.String()


with app.app_context():
    db.create_all()


@app.route("/birthday/")
def index():
    """
    Retrieves all birthdays.

    Returns:
        response (list): A list of dictionaries representing the birthdays.
    """
    birthdays = Birthday.query.all()
    response = []
    for birthday in birthdays:
        response.append({
            "friend_id": birthday.friend_id,
            "fio": birthday.fio,
            "date": birthday.date,
            "wish": birthday.wish
        })
    return jsonify(response)


@app.route("/birthday/<int:friend_id>")
def birthday_by_friend_id(friend_id):
    """
    Retrieves a specific birthdays by friend ID.

    Args:
        friend_id (int): The ID of the friend to retrieve.

    Returns:
        response (dict): A dictionary representing the birthday.
        status_code (int): The HTTP status code.
    """
    birthday = Birthday.query.get(friend_id)
    return jsonify({
        "friend_id": birthday.friend_id,
        "fio": birthday.fio,
        "date": birthday.date,
        "wish": birthday.wish
    }), 200


@app.route("/birthday", methods=["POST"])
def register():
    """
    Creates a new birthday.

    Returns:
        response (dict): A dictionary containing the fio, date and wish of the created birthday.
        status_code (int): The HTTP status code.
    """
    new_birthday = request.json
    # if not new_birthday or "fio" not in new_birthday or "date" not in new_birthday or 'wish' in new_birthday:
    #     return jsonify({"error": "invalid note ID request"}), 400
    if not new_birthday:
        return jsonify({"error": "invalid request"}), 400
    if "fio" not in new_birthday:
        return jsonify({"error": "invalid request"}), 400
    if "date" not in new_birthday:
        return jsonify({"error": "invalid request"}), 400
    if "wish" not in new_birthday:
        return jsonify({"error": "invalid request"}), 400

    try:
        date_str = new_birthday["date"]
        date = datetime.strptime(date_str, "%d.%m.%Y").date()

        birthday = Birthday(
            fio=new_birthday["fio"],
            date=date,
            wish=new_birthday['wish']
        )

        db.session.add(birthday)
        db.session.commit()

        return jsonify({"message": "Birthday created successfully"}), 201
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400
    except IntegrityError:
        return jsonify({"error": "Birthday already exists"})


@app.route('/birthday/<int:friend_id>', methods=["PUT"])
def update_birthday(friend_id):
    """
    Changes all fields in birthday by friend_id.

    Returns:
        response (dict): A dictionary containing the fio, date and wish of the changed birthday.
        status_code (int): The HTTP status code.
    """
    try:
        birthday = db.session.get(Birthday, friend_id)
        if birthday is None:
            return jsonify({"error": "Birthday not found"}), 404

        req_json = request.json

        birthday.fio = req_json.get('fio')
        birthday.date = datetime.strptime(req_json.get('date'),"%d.%m.%Y").date()
        birthday.wish = req_json.get('wish')

        db.session.add(birthday)
        db.session.commit()

        return jsonify({
            "friend_id": birthday.friend_id,
            "fio": birthday.fio,
            "date": birthday.date.strftime("%d.%m.%Y"),
            "wish": birthday.wish
        }), 204
    except Exception:
        return {"message": "error"}, 404

@app.route('/birthday/<int:friend_id>', methods=["DELETE"])
def delete(friend_id):
    """
    Changes all fields in birthday by friend_id.

    Returns:
        response (str): Result of function: "deleted" or error.
        status_code (int): The HTTP status code.
    """
    try:
        birthday = Birthday.query.get(friend_id)
        db.session.delete(birthday)
        db.session.commit()
        return f'You have deleted birtday of friend whose id is {friend_id}', 200
    except Exception:
        return {"message": "error"}, 404



if __name__ == "__main__":
    app.run(debug=True)