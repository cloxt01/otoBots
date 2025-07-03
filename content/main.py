import time
from graphql_client import GraphQLClient
from product_monitor import ProductMonitor
from cart_manager import CartManager
from checkout_handler import CheckoutHandler

class FlashSaleBot:
    def __init__(self):
        self.client = GraphQLClient()
        self.monitor = ProductMonitor(self.client)
        self.cart = CartManager(self.client)
        self.checkout = CheckoutHandler(self.client)

    def run(self):
        product_data = self.monitor.watch_product()
        if product_data['available']:
            cart_response = self.cart.add_to_cart(product_data)
            if cart_response['success']:
                self.checkout.process_checkout()

if __name__ == '__main__':
    bot = FlashSaleBot()
    bot.run()