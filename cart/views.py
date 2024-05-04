from django.shortcuts import render
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from decimal import Decimal

def cart_summary(request):
    return render(request, 'cart/cart-summary.html')

def cart_add(request):
    if request.POST.get('action') == 'post':
        cart = Cart(request)
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_quantity'))
        product = Product.objects.filter(id=product_id)[0]
        if product:
            cart.add(product, product_qty)
            return JsonResponse({"qty":  cart.__len__()}, status=200)
        return JsonResponse({"msg": "Product not found"}, status=500)




def cart_delete(request):
    if request.POST.get('action') == 'post':
        cart = Cart(request)
        product_id = int(request.POST.get('product_id'))
        product = Product.objects.filter(id=product_id)[0]
        if product:
            cart.delete(product_id)
            return JsonResponse({"qty":  cart.__len__(), "total": cart.get_total()}, status=200)
        return JsonResponse({"msg": "Invalid Product"}, status=500)




def cart_update(request):
    if request.POST.get('action') == 'post':
        cart = Cart(request)
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_quantity'))
        print(product_qty)
        product = Product.objects.filter(id=product_id)[0]
        if product:
            cart.update(product_id, product_qty)
            return JsonResponse({"qty":  cart.__len__(), "total": cart.get_total()}, status=200)
        return JsonResponse({"msg": "Invalid Product"}, status=500)
