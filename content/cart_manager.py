class CartManager:
    def __init__(self, client):
        self.client = client

    def add_to_cart(self, product_data):
        variables = {
            'items': [{
                'productID': product_data['id'],
                'warehouseID': product_data['warehouse_id'],
                'quantity': 1,
                'parentID': product_data['parent_id']
            }]
        }
        response = self.client.post('AddToCartOCCMulti', variables)
        return {
            'success': 'data' in response,
            'cart_id': response.get('data', {}).get('add_to_cart_occ_multi', {}).get('data', {}).get('carts', [{}])[0].get('cart_id')
        }