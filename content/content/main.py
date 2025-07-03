import time
from product_monitor import check_product_availability
from checkout import add_to_cart_and_checkout

PRODUCT_URL = "https://www.tokopedia.com/sania/t-shirt-wanita-lengan-pendek"
REFRESH_INTERVAL = 0.5  # 500ms

if __name__ == "__main__":
    while True:
        product_id, stock_status = check_product_availability(PRODUCT_URL)
        
        if stock_status == "available":
            print(f"Stok tersedia! Produk ID: {product_id}")
            add_to_cart_and_checkout(product_id)
            break
        elif stock_status == "low_stock":
            print(f"Stok hampir habis! Mencoba checkout cepat...")
            add_to_cart_and_checkout(product_id)
            break
        
        time.sleep(REFRESH_INTERVAL)