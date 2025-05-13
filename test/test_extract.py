import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
import requests

from utils.extract import scrape_collection_data, fetch_page_content, extract_collection_data

class TestExtractFunctions(unittest.TestCase):

    @patch('utils.extract.requests.get')
    def test_fetch_page_content_success(self, mock_get):
        """Test fetch_page_content berhasil mengembalikan HTML"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body>Test content</body></html>"
        mock_get.return_value = mock_response

        result = fetch_page_content("https://fashion-studio.dicoding.dev")
        self.assertIn("Test content", result)

    @patch('utils.extract.requests.get')
    def test_fetch_page_content_failure(self, mock_get):
        """Test fetch_page_content gagal karena exception"""
        mock_get.side_effect = requests.exceptions.RequestException("Gagal mengambil halaman")

        result = fetch_page_content("https://fashion-studio.dicoding.dev")
        self.assertIsNone(result)

    @patch('builtins.open')
    @patch('json.load')
    def test_extract_collection_data_from_json(self, mock_json_load, mock_open):
        # Setup mock data
        mock_json_data = {
            "product_title": 'Unknown Product',
            "price" : "$100.00",
            "ratings" :  "⭐ Invalid  Rating",
            "colors" : "5 Colors",
            "size"  : "M",
            "gender" : "Men"
        }

        # Atur mock agar json.load mengembalikan data di atas
        mock_json_load.return_value = mock_json_data

        # Simulasikan proses membaca file JSON
        with open("test/sample_product.json") as f:
            data = mock_json_load(f)

        # Buat HTML dari mock data
        html = f"""
            <div class="collection-card">
                <h3 class="product-title">{data['product_title']}</h3>
                <span class="price">{data['price']}</span>
                <p>Rating: {data['ratings']}</p>
                <p>Colors: {data['colors']}</p>
                <p>Size: {data['size']}</p>
                <p>Gender: {data['gender']}</p>
            </div>
            """

        # Parsing HTML dan panggil fungsi yang diuji
        div = BeautifulSoup(html, "html.parser").find("div", class_="collection-card")
        result = extract_collection_data(div)

        # Assertion sama seperti sebelumnya
        self.assertEqual(result["product_title"], data["product_title"])
        self.assertEqual(result["price"], data["price"])
        self.assertEqual(result["ratings"], data["ratings"].split("/")[0])
        self.assertEqual(result["colors"], f"Colors: {data['colors']}")
        self.assertEqual(result["size"], data["size"])
        self.assertEqual(result["gender"], data["gender"])
        self.assertIn("timestamp", result)

    @patch('utils.extract.fetch_page_content')
    def test_scrape_collection_data_one_product(self, mock_fetch):
        """Test scrape_collection_data mengembalikan satu produk"""
        html = """
        <div class="collection-card">
            <h3 class="product-title">Product A</h3>
            <span class="price">$99.99</span>
            <p>Rating: 4/5</p>
            <p>Colors: Red</p>
            <p>Size: Medium</p>
            <p>Gender: Unisex</p>
        </div>
        """  # Pastikan hanya ada satu produk

        # Mocking response untuk fetch_page_content
        mock_fetch.return_value = f"<html><body>{html}</body></html>"

        url = "https://example.com"
        result = scrape_collection_data(url)

        # Pastikan hanya satu produk yang dikembalikan
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["product_title"], "Product A")
        self.assertEqual(result[0]["price"], "$99.99")
        self.assertEqual(result[0]["ratings"], "4")  # Angka ratingnya
        self.assertEqual(result[0]["colors"], "Colors: Red")
        self.assertEqual(result[0]["size"], "Medium")
        self.assertEqual(result[0]["gender"], "Unisex")
        self.assertIn("timestamp", result[0])

    @patch('utils.extract.fetch_page_content')
    def test_scrape_collection_data_no_products(self, mock_fetch):
        """Test scrape_collection_data saat tidak ada produk"""
        mock_fetch.return_value = "<html><body><p>No products here</p></body></html>"

        url = "https://fashion-studio.dicoding.dev"
        result = scrape_collection_data(url)

        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
