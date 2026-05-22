from django.shortcuts import render, redirect, get_object_or_404
from accounts.decorators import admin_required
from .models import Product, Category, ProductImage
from .forms import ProductForm, CategoryForm


@admin_required
def admin_products(request):
    products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all().order_by('-created_at')
    product_form = ProductForm()
    category_form = CategoryForm()
    if request.method == 'POST':
        if 'add_product' in request.POST:
            product_form = ProductForm(request.POST, request.FILES)
            if product_form.is_valid():
                product = product_form.save()
                product_form.save_extra_images(product)
                return redirect('admin_products')
        elif 'edit_product' in request.POST:
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, pk=product_id)
            product_form = ProductForm(request.POST, request.FILES, instance=product)
            if product_form.is_valid():
                product = product_form.save()
                product_form.save_extra_images(product)
                return redirect('admin_products')
        elif 'delete_product' in request.POST:
            product_id = request.POST.get('product_id')
            Product.objects.filter(pk=product_id).delete()
            return redirect('admin_products')
        elif 'add_category' in request.POST:
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                category_form.save()
                return redirect('admin_products')
        elif 'delete_category' in request.POST:
            category_id = request.POST.get('category_id')
            Category.objects.filter(pk=category_id).delete()
            return redirect('admin_products')
        elif 'delete_image' in request.POST:
            img_id = request.POST.get('image_id')
            ProductImage.objects.filter(pk=img_id).delete()
            return redirect('admin_products')
    return render(request, 'admin_panel/products.html', {
        'products': products,
        'categories': categories,
        'product_form': product_form,
        'category_form': category_form,
    })
