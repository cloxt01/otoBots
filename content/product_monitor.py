import time

class ProductMonitor:
    def __init__(self, client):
        self.client = client

    def watch_product(self):
        while True:
            data = self._get_product_data()
            if data and data['stock'] > 0:
                return data
            time.sleep(5)

    def _get_product_data(self):
        response = self.client.post('PDPGetDataP2', {'productID': '12762995513'})
        pdp_data = response.get('data', {}).get('pdpGetData', {})
        return {
            'id': '12762995513',
            'warehouse_id': '9227548',
            'parent_id': '12762995510',
            'stock': int(pdp_data.get('nearestWarehouse', [{}])[0].get('stock', 0)),
            'available': pdp_data.get('cartRedirection', {}).get('data', [{}])[0].get('available_buttons', []) != []
        }