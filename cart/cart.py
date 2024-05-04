from store.models import Product
from decimal import Decimal
import copy


class Cart:
    def __init__(self, request):
        self.session = request.session
        if 'session_key' in self.session:
            self.cart = self.session.get('session_key')
        else:
            self.cart = self.session['session_key'] = {}
    
    def add(self, product, product_qty):
        if str(product.id) in self.cart:
            self.cart[str(product.id)]['qty'] = product_qty
        else:
            self.cart[str(product.id)] = {'price': str(product.price), 'qty': product_qty}
        
        self.session.modified = True
    

    def delete(self, product_id):
        if str(product_id) in self.cart:
            del self.cart[str(product_id)]
            self.session.modified = True
        return
    
    def update(self, product_id, product_qty):
        if str(product_id) in self.cart:
            self.cart[str(product_id)]['qty'] = product_qty
            self.session.modified = True
        return

    

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())
    
    def __iter__(self):
        all_products_ids = self.cart.keys()
        products = Product.objects.filter(id__in=all_products_ids)
        cart = copy.deepcopy(self.cart)
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total'] = item['price'] * item['qty']
            yield item
        
    def get_total(self):
        total = 0
        for item in self.cart.values():
            total += item['qty'] * Decimal(item['price'])
        
        return total
    
    def get_total_INR_to_USD(self):
        total = self.get_total()
        return  round(total * Decimal(0.012), 2)
        

