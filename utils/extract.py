import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    "User-Agent" : (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}


def extract_collection_data(div):
    """fungsi untuk mengekstrak data dari tag html """
    product_title_tag = div.find("h3", class_="product-title")
    product_title = product_title_tag.get_text(strip=True) if product_title_tag else "Tidak tersedia"

    price_tag = div.find("span", class_="price")
    price = price_tag.get_text(strip=True) if price_tag else "Tidak tersedia"
    
    # scraping data yang ada di tag <p>
    p_tags = div.find_all('p')

    rating = p_tags[0].text.strip().split('/')[0].replace('Rating: ', '') if len(p_tags) > 0 else 'N/A'
    colors = p_tags[1].text.strip()
    size = p_tags[2].text.strip().replace("Size: ", "")
    gender = p_tags[3].text.strip().replace("Gender: ", "")

    # return waktu sekarang
    timestamp = datetime.now().isoformat()

    return {
        "product_title" : product_title,
        "price" : price,
        "ratings" : rating,
        "colors" : colors,
        "size" : size,
        "gender" : gender,
        "timestamp": timestamp
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

    while page <= 50:
        # Mendefinisikan url untuk setiap halaman yang akan di scraping
        if (page == 1) :
            current_url = url # url pertama memiliki format yang berbeda
        else: 
            current_url = f"{url}/page{page}"
            # print(current_url) # ini aku pakai untuk mengecek url

        content = fetch_page_content(current_url)
        
        if not content:
            break

        soup = BeautifulSoup(content, 'html.parser')
        cards = soup.find_all('div', class_='collection-card') # mencari elemen produk di dalam class 'collection-card'

        if not cards: # berhenti scraping jika produk tidak ada
            break
        
        # Ambil data produk dari setiap card
        for card in cards:
            collection_data = extract_collection_data(card)
            data.append(collection_data)

        page += 1 # melanjutkan ke halaman berikutnya

    return data