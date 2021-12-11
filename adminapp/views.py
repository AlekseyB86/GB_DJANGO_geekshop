from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import ShopUserAdminEditForm, AdminProductUpdateForm, AdminProductCategoryUpdateForm
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


class ShopUserListView(SuperUserOnlyMixin, PageTitleMixin, ListView):
    model = ShopUser
    page_title = 'пользователи'


class ShopUserCreateView(SuperUserOnlyMixin, PageTitleMixin, CreateView):
    model = ShopUser
    template_name = 'adminapp/user_form.html'
    form_class = ShopUserRegisterForm
    page_title = 'пользователи/создание'

    def get_success_url(self):
        return reverse('adminapp:user_list')


class ShopUserUpdateView(SuperUserOnlyMixin, PageTitleMixin, UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_form.html'
    form_class = ShopUserAdminEditForm
    page_title = 'пользователи/редактирование'

    def get_success_url(self):
        return reverse('adminapp:user_list')


class ShopUserDeleteView(SuperUserOnlyMixin, PageTitleMixin, DeleteView):
    model = ShopUser
    page_title = 'пользователи/удаление/восстановление'

    def get_success_url(self):
        return reverse('adminapp:user_list')


class ProductCategoryListView(SuperUserOnlyMixin, PageTitleMixin, ListView):
    model = ProductCategory
    page_title = 'категории'


class ProductCategoryCreateView(SuperUserOnlyMixin, PageTitleMixin, CreateView):
    model = ProductCategory
    success_url = reverse_lazy('adminapp:category_list')
    form_class = AdminProductCategoryUpdateForm
    page_title = 'категории/создание'


class ProductCategoryUpdateView(SuperUserOnlyMixin, PageTitleMixin, UpdateView):
    model = ProductCategory
    success_url = reverse_lazy('adminapp:category_list')
    form_class = AdminProductCategoryUpdateForm
    page_title = 'категории/редактирование'


class ProductCategoryDeleteView(SuperUserOnlyMixin, PageTitleMixin, DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('adminapp:category_list')
    page_title = 'категории/удаление'

    def get_success_url(self):
        category_item = ProductCategory.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:category_list')

    # delete переопределяется в models.py
    # def delete(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     self.object.is_active = False
    #     self.object.save()
    #     return HttpResponseRedirect(self.get_success_url())


class ProductCreateView(SuperUserOnlyMixin, PageTitleMixin, CreateView):
    model = Product
    form_class = AdminProductUpdateForm
    page_title = 'продукты/создание'

    def get_success_url(self):
        return reverse('adminapp:product_list', args=[self.kwargs['pk']])


class ProductListView(SuperUserOnlyMixin, PageTitleMixin, ListView):
    paginate_by = 5
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
    form_class = AdminProductUpdateForm

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])


class ProductDeleteView(SuperUserOnlyMixin, PageTitleMixin, DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])

    # delete переопределяется в models.py
    # def delete(self, request, *args, **kwargs):
    #     self.object.is_active = not self.object.is_active
    #     self.object.save()
    #
    #     return HttpResponseRedirect(reverse('adminapp:product_list', args=[self.object.category_id]))


class ProductDetailView(SuperUserOnlyMixin, PageTitleMixin, DetailView):
    model = Product
    page_title = 'продукты/подробнее'
