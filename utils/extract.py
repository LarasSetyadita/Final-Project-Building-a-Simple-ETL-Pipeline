import requests
import pandas as pd
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent" : (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def extract_collection_data(div):
    product_title_tag = div.find("h3", class_="product-title")
    product_title = product_title_tag.get_text(strip=True) if product_title_tag else "Tidak tersedia"

    price_tag = div.find("span", class_="price")
    price = price_tag.get_text(strip=True) if price_tag else "Tidak tersedia"

    p_tags = div.find_all('p')
    if len(p_tags) >= 4:
        colors = p_tags[1].text.strip()
        size = p_tags[2].text.strip().replace("Size: ", "")
        gender = p_tags[3].text.strip().replace("Gender: ", "")
    else:
        colors = size = gender = None

    return {
        "product_title" : product_title,
        "price" : price,
        "colors" : colors,
        "size" : size,
        "gender" : gender
    }

def fetch_page_content(url):
    """Mengambil konten HTML dari URL dengan user-agent yang ditentukan."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error saat mengambil {url}: {e}")
        return None

def scrape_collection_data(url):
    """Melakukan scraping semua data dari halaman koleksi produk, termasuk halaman berikutnya."""
    data = []
    page = 1  # Mulai dari halaman pertama

    while True:
        # Bangun URL untuk setiap halaman

        if (page == 1) :
            current_url = url
        else: 
            current_url = f"{url}/page{page}"
            print(current_url)

        content = fetch_page_content(current_url)
        
        if not content:
            break  # Jika konten tidak ditemukan (misalnya halaman tidak ada), berhenti

        soup = BeautifulSoup(content, 'html.parser')
        
        # Temukan semua elemen produk dengan class 'collection-card'
        cards = soup.find_all('div', class_='collection-card')

        # Jika tidak ada produk pada halaman, berhenti
        if not cards:
            break
        
        # Ambil data produk dari setiap card
        for card in cards:
            collection_data = extract_collection_data(card)
            data.append(collection_data)
        
        # Lanjutkan ke halaman berikutnya
        page += 1

    return data

def main():
    """Fungsi utama untuk menjalankan proses scraping dan menyimpan data."""
    url = 'https://fashion-studio.dicoding.dev'
    collection_data = scrape_collection_data(url)
 
    if collection_data:
        # Jika data berhasil diambil, simpan dalam DataFrame dan tampilkan
        df = pd.DataFrame(collection_data)
        print(df)
    else:
        print("Tidak ada data yang ditemukan.")

if __name__ == "__main__":
    main()
