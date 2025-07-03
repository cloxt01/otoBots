import requests
import json

def add_to_cart_and_checkout(product_id):
    # Autentikasi (simulasi session)
    SESSION_COOKIE = "_abck=YOUR_SESSION_COOKIE; DID=YOUR_DEVICE_ID"
    
    graphql_url = "https://gql.tokopedia.com/graphql"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Android 4.4; Mobile; rv:70.0) Gecko/70.0 Firefox/70.0",
        "Cookie": SESSION_COOKIE
    }
    
    # Mutasi GraphQL untuk tambahkan ke keranjang
    add_to_cart_mutation = {
        "operationName": "AddToCartOCCMulti",
        "variables": {
            "input": [{
                "productID": product_id,
                "quantity": 1,
                "warehouseID": "19143024"  # ID gudang dari traffic
            }]
        },
        "query": "mutation AddToCartOCCMulti($input: [AddToCartInput!]!) {\n  add_to_cart_occ_multi(input: $input) {\n    data {\n      carts {\n        cart_id\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}"
    }
    
    try:
        # Step 1: Tambahkan ke keranjang
        cart_response = requests.post(graphql_url, headers=headers, data=json.dumps(add_to_cart_mutation))
        cart_response.raise_for_status()
        print("Produk berhasil ditambahkan ke keranjang!")
        
        # Step 2: Lanjutkan ke checkout (simulasi)
        print("Melakukan proses checkout...")
        # Di sini bisa ditambahkan logika checkout lengkap
        
    except requests.RequestException as e:
        print(f"Checkout gagal: {str(e)}")