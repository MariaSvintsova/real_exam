
import unittest
from datetime import datetime

from flask import Flask
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy

from app import app, db, Birthday


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self._ctx = app.test_request_context()
        self._ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self._ctx.pop()

    def test_index(self):
        response = self.app.get("/birthday/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])
        print(response.json)

        expected_response = []
        actual_response = response.json



        self.assertEqual(expected_response, actual_response)


    def test_birthday_by_friend_id(self):
        # Add test data
        friend_id = 7
        date = datetime.strptime("09.09.2001", "%d.%m.%Y").date()
        birthday = Birthday(friend_id=friend_id, fio="John Doe", date=date, wish="cake")
        db.session.add(birthday)
        db.session.commit()

        # Perform the test
        response = self.app.get(f"/birthday/{friend_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "friend_id": birthday.friend_id,
            "fio": birthday.fio,
            "date": birthday.date.strftime("%a, %d %b %Y %H:%M:%S GMT"),
            "wish": birthday.wish
        })


    def test_delete(self):
        friend_id = 10
        date = datetime.strptime("01.09.2001", "%d.%m.%Y").date()
        birthday = Birthday(friend_id=friend_id, fio="John Golt", date=date, wish="valley")
        db.session.add(birthday)
        db.session.commit()

        response = self.app.delete(f"/birthday/{birthday.friend_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), f"You have deleted birtday of friend whose id is {birthday.friend_id}")

        deleted_note = Birthday.query.get(birthday.friend_id)
        self.assertIsNone(deleted_note)


    # def test_put(self):
    #     friend_id = 17
    #     date = datetime.strptime("01.09.2001", "%d.%m.%Y").date()
    #     birthday = Birthday(friend_id=friend_id, fio="John Okley", date=date, wish="world")
    #     db.session.add(birthday)
    #     db.session.commit()
    #
    #     new_data = {"fio": birthday.fio, "date": date, "wish": birthday.wish}
    #     response = self.app.put(f"/birthday/{friend_id}", json=new_data)
    #     print(response)
    #     self.assertEqual(response.status_code, 204)
    #
    #     updated_birthday = Birthday.query.get(birthday.friend_id)
    #     self.assertEqual(updated_birthday.fio, new_data["fio"])
    #     self.assertEqual(updated_birthday.date, new_data["date"])
    #     self.assertEqual(updated_birthday.wish, new_data["wish"])

    # def test_post(self):
    #     date = datetime.strptime("01.08.2001", "%d.%m.%Y").date()
    #     data = {"fio":"John OOp", "date": date, "wish":"book"}
    #     response = self.app.post("/birthday", json=data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json, {"fio": data["fio"], "date": data["date"], "wish": data["wish"]})
    #
    #     day = Birthday.query.first()
    #     self.assertEqual(day.fio, data["fio"])
    #     self.assertEqual(day.wish, data["wish"])

if __name__ == "__main__":
    unittest.main()
