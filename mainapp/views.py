import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def get_hot_product():
    return random.sample(list(Product.objects.all()), 1)[0]


def get_same_products(hot_product):
    return Product.objects.filter(category=hot_product.category).exclude(
        pk=hot_product.pk
    )[:3]


def get_links_menu():
    return ProductCategory.objects.all()


def index(request):
    context = {
        'title': 'Главная',
        'products': Product.objects.all()[:4],
    }
    return render(request, 'mainapp/index.html', context=context)


def contact(request):
    context = {
        'title': 'Контакты',
    }
    return render(request, 'mainapp/contact.html', context=context)


def products(request, pk=None, page=1):
    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all()
            category_item = {
                'name': 'все',
                'pk': 0
            }
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk)

        # Пагинация
        # page = request.GET.get('p', 1)  # если page не передаётся в функции
        paginator = Paginator(products_list, 6)
        try:
            product_paginator = paginator.page(page)
        except PageNotAnInteger:
            # если не интовый номер страницы отдаем 1ю страницу, много дублей страниц
            product_paginator = paginator.page(1)
        except EmptyPage:
            # если номер больше числа страниц отдаем последнюю страницу, много дублей страниц
            product_paginator = paginator.page(paginator.num_pages)
        context = {
            'links_menu': get_links_menu(),
            'title': 'Продукты',
            'category': category_item,
            'products': product_paginator,
        }
        return render(request, 'mainapp/products_list.html', context=context)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    context = {
        'links_menu': get_links_menu(),
        'title': 'Продукты',
        'hot_product': hot_product,
        'same_products': same_products,
    }
    return render(request, 'mainapp/products.html', context=context)


def product(request, pk):
    context = {
        'product': get_object_or_404(Product, pk=pk),
        'links_menu': get_links_menu()
    }
    return render(request, 'mainapp/product.html', context)
