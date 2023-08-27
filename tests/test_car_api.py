import flask_unittest

from website.database import Database
from __main__ import create_app

class TestAPICars(flask_unittest.ClientTestCase):
    app = create_app()
    def get_cars(self, client):
        resp = client.get('/api/terms')
        self.assertEqual(resp.status_code, 200)

        json = resp.json

        self.assertIsNotNone(json)
        