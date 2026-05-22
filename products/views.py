from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def home_view(request):
    products = Product.objects.all().order_by('-created_at')
    category_id = request.GET.get('category')
    search = request.GET.get('search')
    if category_id:
        products = products.filter(category_id=category_id)
    if search:
        products = products.filter(name__icontains=search)
    categories = Category.objects.all()
    return render(request, 'products/home.html', {
        'products': products,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
        'search': search or '',
    })


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related,
    })
