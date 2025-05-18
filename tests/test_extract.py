import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
import requests

from utils.extract import scrape_collection_data, fetch_page_content, extract_collection_data

class TestExtractFunctions(unittest.TestCase):

    def setUp(self):
        self.url = "https://fashion-studio.dicoding.dev/"

    @patch('utils.extract.requests.get')
    def test_fetch_page_content_success(self, mock_get):
        """Test fetch_page_content berhasil mengembalikan HTML"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body>Test content</body></html>"

        mock_get.return_value = mock_response

        result = fetch_page_content("http://dummy-url.com")
        self.assertIn("Test content", result)

    @patch('utils.extract.requests.get')
    def test_fetch_page_content_failure(self, mock_get):
        """Test fetch_page_content gagal karena exception"""
        mock_get.side_effect = requests.exceptions.RequestException("Gagal mengambil halaman")

        result = fetch_page_content(self.url)
        self.assertIsNone(result)

    def test_extract_collection_data(self):
        """Test extract_collection_data dari HTML buatan"""
        mock_data = {
            "product_title": 'T-shirt 2',
            "price": "1634400.0",
            "ratings": "3.9",
            "colors": "3",
            "size": "M",
            "gender": "Women"
        }

        html = f"""
        <div class="collection-card">
            <h3 class="product-title">{mock_data['product_title']}</h3>
            <span class="price">{mock_data['price']}</span>
            <p>Rating: {mock_data['ratings']}</p>
            <p>{mock_data['colors']}</p>
            <p>Size: {mock_data['size']}</p>
            <p>Gender: {mock_data['gender']}</p>
        </div>
        """

        div = BeautifulSoup(html, "html.parser").find("div", class_="collection-card")
        result = extract_collection_data(div)

        self.assertEqual(result["product_title"], mock_data["product_title"])
        self.assertEqual(result["price"], mock_data["price"])
        self.assertEqual(result["ratings"], mock_data["ratings"].split("/")[0].replace("Rating: ", "").strip("⭐ "))
        self.assertEqual(result["colors"], mock_data["colors"])
        self.assertEqual(result["size"], mock_data["size"])
        self.assertEqual(result["gender"], mock_data["gender"])
        self.assertIn("timestamp", result)

    @patch('utils.extract.fetch_page_content')
    def test_scrape_collection_data_one_product(self, mock_fetch):
        def test_scrape_collection_data_one_product(self, mock_fetch):
            mock_html = """
            <html><body>
                <div class="collection-card">
                    <h3 class="product-title">Kaos Uji</h3>
                    <div class="price-container">$100000</div>
                    <p>Rating: ⭐ 4.5/5</p>
                    <p>Colors: 2</p>
                    <p>Size: L</p>
                    <p>Gender: Unisex</p>
                </div>
            </body></html>
            """
            mock_fetch.return_value = mock_html
            result = scrape_collection_data(self.url)

            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["product_title"], "Kaos Uji")

    @patch('utils.extract.fetch_page_content')
    def test_scrape_collection_data_no_products(self, mock_fetch):
        """Test scrape_collection_data saat tidak ada produk"""
        mock_fetch.return_value = "<html><body><p>No products here</p></body></html>"

        result = scrape_collection_data(self.url)

        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
