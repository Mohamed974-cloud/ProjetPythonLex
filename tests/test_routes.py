### `tests/test_routes.py`
import unittest
from app import create_app

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_upload_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bienvenue sur l\'application Flask', response.data)

if __name__ == '__main__':
    unittest.main()