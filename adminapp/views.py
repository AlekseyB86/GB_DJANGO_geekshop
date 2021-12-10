from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from adminapp.forms import ShopUserAdminEditForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


class SuperUserOnlyMixin:
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class PageTitleMixin:
    page_title = ''

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = self.page_title
        return context_data


class UserCreateView(SuperUserOnlyMixin, PageTitleMixin, CreateView):
    model = ShopUser
    template_name = 'adminapp/user_form.html'
    form_class = ShopUserRegisterForm
    page_title = 'пользователи/создание'

    def get_success_url(self):
        return reverse('adminapp:user_list')


class ShopUserListView(SuperUserOnlyMixin, PageTitleMixin, ListView):
    model = ShopUser
    page_title = 'пользователи'


class UserUpdateView(SuperUserOnlyMixin, PageTitleMixin, UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_form.html'
    form_class = ShopUserAdminEditForm
    page_title = 'пользователи/редактирование'

    def get_success_url(self):
        return reverse('adminapp:user_list')


# @user_passes_test(lambda u: u.is_superuser)
# def user_delete(request, pk):
#     current_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         current_user.is_active = not current_user.is_active
#         current_user.save()
#         return HttpResponseRedirect(reverse('adminapp:user_list'))
#
#     context = {
#         'title': 'пользователи/удаление',
#         'object': current_user
#     }
#     return render(request, 'adminapp/user_delete.html', context)


class UserDeleteView(SuperUserOnlyMixin, PageTitleMixin, DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    page_title = 'пользователи/удаление/восстановление'

    def get_success_url(self):
        return reverse('adminapp:user_list')


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


class ProductCreateView(SuperUserOnlyMixin, PageTitleMixin, CreateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductEditForm

    def get_success_url(self):
        # print(reverse('adminapp:product_list', args=[self.kwargs['pk']]))
        return reverse('adminapp:product_list', args=[self.kwargs['pk']])


class ProductListView(SuperUserOnlyMixin, PageTitleMixin, ListView):
    model = Product
    template_name = 'adminapp/products.html'
    page_title = 'продукты'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['category'] = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        return context_data

    def get_queryset(self):
        return Product.objects.filter(category__pk=self.kwargs.get('pk'))  # достаем pk который передается в urls


class ProductUpdateView(SuperUserOnlyMixin, PageTitleMixin, UpdateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductEditForm

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])


class ProductDeleteView(SuperUserOnlyMixin, PageTitleMixin, DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])

    # delete переопределяется либо здесь либо в models.py
    # def delete(self, request, *args, **kwargs):
    #     self.object.is_active = not self.object.is_active
    #     self.object.save()
    #
    #     return HttpResponseRedirect(reverse('adminapp:product_list', args=[self.object.category_id]))


class ProductDetailView(SuperUserOnlyMixin, PageTitleMixin, DeleteView):
    model = Product
    template_name = 'adminapp/product_detail.html'
