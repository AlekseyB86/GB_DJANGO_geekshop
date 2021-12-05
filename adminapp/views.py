from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    context = {

    }
    return render(request, '', context)


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    context = {
        'title': 'админка/пользователи',
        'object_list': ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
    }
    return render(request, 'adminapp/users.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request):
    context = {

    }
    return render(request, '', context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request):
    context = {

    }
    return render(request, '', context)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    context = {

    }
    return render(request, '', context)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    context = {
        'title': 'админка/категории',
        'object_list': ProductCategory.objects.all().order_by('-is_active')
    }
    return render(request, 'adminapp/categories.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request):
    context = {

    }
    return render(request, '', context)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request):
    context = {

    }
    return render(request, '', context)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request):
    context = {

    }
    return render(request, '', context)


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    context = {
        'title': 'админка/продукты',
        'category': get_object_or_404(ProductCategory, pk=pk),
        'object_list': Product.objects.filter(category__pk=pk).order_by('-is_active')
    }
    return render(request, 'adminapp/products.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request):
    context = {

    }
    return render(request, '', context)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request):
    context = {

    }
    return render(request, '', context)


@user_passes_test(lambda u: u.is_superuser)
def product_detail(request):
    context = {

    }
    return render(request, '', context)
