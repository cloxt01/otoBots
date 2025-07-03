class CheckoutHandler:
    def __init__(self, client):
        self.client = client

    def process_checkout(self):
        self._select_shipping()
        self._process_payment()

    def _select_shipping(self):
        shipping_data = {
            'logisticOption': {
                'tts_id': '7133128197851318017',
                'insurance': True
            }
        }
        return self.client.post('UpdateShippingMethod', shipping_data)

    def _process_payment(self):
        payment_data = {
            'paymentMethod': {
                'code': 'BCAVA',
                'metadata': '...'
            }
        }
        return self.client.post('SubmitCheckout', payment_data)