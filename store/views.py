from django.shortcuts import render
from .models import Category, Product
from django.shortcuts import get_object_or_404

def store(request):
    all_product = Product.objects.all()
    return render(request, 'store/store.html', {'all_product': all_product})


def categories(request):
    all_categories = Category.objects.all()
    return {'all_categories': all_categories}

def product_info(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    return render(request, 'store/product-info.html', {'product': product})

def list_product(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/list-category.html', {'products': products, 'category': category})
