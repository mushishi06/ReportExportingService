import json

import unittest

from app import app


class MyTests(unittest.TestCase):
    """Main test class."""

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """Setup test app."""
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    def test_index_status_code(self):
        """Test server running."""
        # sends HTTP GET request to the application on the specified path
        result = self.app.get('/')
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_index_data(self):
        """Test of index root data."""
        result = self.app.get('/')
        usage = b'Usage: /reports/{int:reports_id} <br>Eg. /reports/2?format=pdf<br>Eg. /reports/2?format=xml<br><br>Usage: /reports <br>Eg. /reports?format=pdf<br>Eg. /reports?format=xml'
        self.assertEqual(result.data, usage)

    def test_home_report(self):
        """Test reports '/reports'."""
        result = self.app.get('/reports')

        self.assertEqual(result.status_code, 200)
        # json = ''
        # self.assertEqual(result.data, json)

    def test_non_existant_report(self):
        """Test non existant id reports."""
        result = self.app.get('/reports/0')
        json_data = json.loads(result.data.decode('utf-8'))

        self.assertEqual(result.status_code, 404)
        self.assertIn('Not Found:http://localhost/reports/0', json_data['message'])
        self.assertEqual(404, json_data['status'])

    def test_existant_report(self):
        """Test non existant id reports."""
        result = self.app.get('/reports/1')
        json_data = json.loads(result.data.decode('utf-8'))

        self.assertEqual(result.status_code, 200)
        self.assertIn('organization', json_data['data'])
        self.assertEqual(1, json_data['id'])

    def test_existant_report_xml(self):
        """Test non existant id reports."""
        result = self.app.get('/reports/1?format=xml')

        self.assertEqual(result.status_code, 200)
        self.assertIn(b'data', result.data)
        self.assertIn(b'organization', result.data)

    def test_existant_report_xml_headers(self):
        """Test non existant id reports."""
        headers = {}
        headers['Content-Type'] = 'text/xml'

        result = self.app.get('/reports/1?format=xml', headers=headers)

        self.assertEqual(result.status_code, 200)
        self.assertIn(b'data', result.data)
        self.assertIn(b'organization', result.data)
        self.assertIn('text/xml', result.headers['Content-Type'])


if __name__ == '__main__':
    unittest.main()
