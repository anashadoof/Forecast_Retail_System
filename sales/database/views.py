from django.shortcuts import render, redirect, get_object_or_404
from .models import Stores, Products, Promo, Sales
from .forms import StoreForm, ProductForm, PromoForm, SalesForm
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required(login_url='login')
def database_home(request):
    stores = Stores.objects.all()
    products = Products.objects.all()
    promos = Promo.objects.all()
    sales = Sales.objects.all().select_related('store', 'product', 'promo').order_by('-date')[:40]
    return render(request, 'database/database_home.html', {'stores': stores,
                                                           "products": products,
                                                           'promos': promos,
                                                           'sales': sales})
@user_passes_test(lambda u: u.is_authenticated and u.is_superuser, login_url='login')
def add_store(request):
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('database_home') + '?tab=stores')
        else:
            return render(request, 'database/add_store.html', {'form': form})
    else:
        form = StoreForm()
    return render(request, 'database/add_store.html', {'form': form})

@user_passes_test(lambda u: u.is_authenticated and u.is_superuser, login_url='login')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('database_home') + '?tab=products')
    else:
        form = ProductForm()
    return render(request, 'database/add_product.html', {'form': form})

@user_passes_test(lambda u: u.is_authenticated and u.is_superuser, login_url='login')
def add_sale(request):
    if request.method == 'POST':
        form = SalesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('database_home') + '?tab=sales')
    else:
        form = SalesForm()
    return render(request, 'database/add_sales.html', {'form': form})

@user_passes_test(lambda u: u.is_authenticated and u.is_superuser, login_url='login')
def add_promo(request):
    if request.method == 'POST':
        form = PromoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('database_home') + '?tab=promo')
    else:
        form = PromoForm()
    return render(request, 'database/add_promo.html', {'form': form})


@require_POST
def delete_store(request, store_id):
    store = get_object_or_404(Stores, store_id=store_id)
    store.delete()
    return redirect(reverse('database_home') + '?tab=stores')

@require_POST
def delete_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Products, product_id=product_id)
        product.delete()
    return redirect(reverse('database_home') + '?tab=products')

@require_POST
def delete_promo(request, promo_id):
    promo = get_object_or_404(Promo, promo_id=promo_id)
    promo.delete()
    return redirect(reverse('database_home') + '?tab=promo')

@require_POST
def delete_sale(request, sale_id):
    sale = get_object_or_404(Sales, pk=sale_id)
    sale.delete()
    return redirect(reverse('database_home') + '?tab=sales')

@user_passes_test(lambda u: u.is_authenticated and u.is_superuser, login_url='login')
def edit_store(request, store_id):
    store = get_object_or_404(Stores, store_id=store_id)
    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store, is_edit=True)
        if form.is_valid():
            form.save()
            return redirect(reverse('database_home') + '?tab=stores')
    else:
        form = StoreForm(instance=store, is_edit=True)
    return render(request, 'database/edit_store.html', {'form': form})

@user_passes_test(lambda u: u.is_authenticated and u.is_superuser, login_url='login')
def edit_product(request, product_id):
    product = get_object_or_404(Products, product_id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product, is_edit=True)
        if form.is_valid():
            form.save()
            return redirect(reverse('database_home') + '?tab=products')
    else:
        form = ProductForm(instance=product, is_edit=True)
    return render(request, 'database/edit_product.html', {'form': form})

@user_passes_test(lambda u: u.is_authenticated and u.is_superuser, login_url='login')
def edit_promo(request, promo_id):
    promo = get_object_or_404(Promo, promo_id=promo_id)
    if request.method == 'POST':
        form = PromoForm(request.POST, instance=promo, is_edit=True)
        if form.is_valid():
            form.save()
            return redirect(reverse('database_home') + '?tab=promo')
    else:
        form = PromoForm(instance=promo, is_edit=True)
    return render(request, 'database/edit_promo.html', {'form': form})

@user_passes_test(lambda u: u.is_authenticated and u.is_superuser, login_url='login')
def edit_sale(request, sale_id):
    sale = get_object_or_404(Sales, id=sale_id)
    if request.method == 'POST':
        form = SalesForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            return redirect(reverse('database_home') + '?tab=sales')
    else:
        form = SalesForm(instance=sale)
    return render(request, 'database/edit_sales.html', {'form': form})
