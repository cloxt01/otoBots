import requests
from bs4 import BeautifulSoup

def check_product_availability(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Android 4.4; Mobile; rv:70.0) Gecko/70.0 Firefox/70.0",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Ekstrak ID produk dari meta tag
        product_id = soup.find("meta", property="og:url")['content'].split("/")[-1]
        
        # Deteksi stok berdasarkan elemen UI
        stock_element = soup.select_one('[aria-label="Jumlah stok"]')
        if stock_element:
            stock_text = stock_element.get_text().lower()
            if 'habis' in stock_text:
                return product_id, "out_of_stock"
            elif 'sisa' in stock_text and int(stock_text.split()[1].replace(',', '')) < 10:
                return product_id, "low_stock"
        
        return product_id, "available"
    
    except requests.RequestException:
        return None, "error"
    except Exception as e:
        print(f"Error monitoring: {str(e)}")
        return None, "error"