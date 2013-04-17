import unittest
import requests
from annie import db
from annie.api.users.models import User


"""
TODO:
    move auth test code to his own methods
    build custom assertions for http responses.
"""


class UserApiTest(unittest.TestCase):

    def setUp(self):
        db.create_all()
        john = User(
            user_name='john',
            user_password='1234',
            user_email='johndoe@gmail.com'
        )
        jane = User(
            user_name='jane',
            user_password='1234',
            user_email='janedoe@gmail.com'
        )
        db.session.add(john)
        db.session.add(jane)
        db.session.commit()

        self.url = 'http://localhost:5000/users/'

    def tearDown(self):
        db.drop_all()

    # GET /users/
    # GET /users/user_id/
    def test_read_user_that_not_exists(self):

        r = requests.get(self.url + '3/')
        self.assertEqual(r.status_code, 404)

    def test_read_user_that_exists(self):

        r = requests.get(self.url + '1/')
        self.assertEqual(r.status_code, 200)

    def test_read_all_users(self):

        r = requests.get(self.url)
        self.assertEqual(r.status_code, 200)

    # POST /users/
    def test_create_user_that_not_exists(self):

        r = requests.post(self.url, data={
            'user_name':     'david',
            'user_password': '1234',
            'user_email':    'davidmills@gmail.com'
        })
        self.assertEqual(r.status_code, 201)

    def test_create_user_that_exists(self):

        r = requests.post(self.url, data={
            'user_name': 'john',
            'user_password': '1234',
            'user_email': 'johndoe@gmail.com'
        })
        self.assertEqual(r.status_code, 409)

    # PUT /users/<name>/
    def test_update_user_that_not_exists(self):

        r = requests.put(self.url + '3/')
        self.assertEqual(r.status_code, 404)

    def test_update_name_of_user_that_exists_name_changes(self):

        r = requests.put(self.url + '1/', data={
            'user_name': 'david'
        })
        self.assertEqual(r.status_code, 301)

    def test_update_name_of_user_that_exists_name_not_changes(self):

        r = requests.put(self.url + '1/', data={
            'user_name': 'john'
        })
        self.assertEqual(r.status_code, 200)

    # DELETE /users/<user_id>/
    def test_delete_user_that_not_exists(self):

        r = requests.delete(self.url + '3/')
        self.assertEqual(r.status_code, 404)

    def test_delete_user_that_exists(self):

        r = requests.delete(self.url + '1/')
        self.assertEqual(r.status_code, 200)

        r = requests.get(self.url + '1/')
        self.assertEqual(r.status_code, 404)
