from django.test import TestCase, Client

# Create your tests here.
class MywatchlistTest(TestCase):
    def test_url_menu_exist(self):
        response = Client().get("/mywatchlist/")
        self.assertEqual(response.status_code, 200)

    def test_url_html_exist(self):
        response = Client().get("/mywatchlist/html/")
        self.assertEqual(response.status_code, 200)

    def test_url_xml_exist(self):
        response = Client().get("/mywatchlist/xml/")
        self.assertEqual(response.status_code, 200)

    def test_url_json_exist(self):
        response = Client().get("/mywatchlist/json/")
        self.assertEqual(response.status_code, 200)