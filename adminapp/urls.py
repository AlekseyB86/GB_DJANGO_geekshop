from django.urls import path
from adminapp import views as admin_views

app_name = 'adminapp'

urlpatterns = [
    path('users/create/', admin_views.ShopUserCreateView.as_view(), name='user_create'),
    path('', admin_views.ShopUserListView.as_view(), name='user_list'),
    path('users/update/<int:pk>/', admin_views.ShopUserUpdateView.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', admin_views.ShopUserDeleteView.as_view(), name='user_delete'),

    path('categories/create/', admin_views.ProductCategoryCreateView.as_view(), name='category_create'),
    path('categories/', admin_views.ProductCategoryListView.as_view(), name='category_list'),
    path('categories/update/<int:pk>/', admin_views.ProductCategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', admin_views.ProductCategoryDeleteView.as_view(), name='category_delete'),

    path('products/create/<int:pk>/', admin_views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/', admin_views.ProductListView.as_view(), name='product_list'),
    path('products/update/<int:pk>/', admin_views.ProductUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', admin_views.ProductDeleteView.as_view(), name='product_delete'),
    path('products/detail/<int:pk>/', admin_views.ProductDetailView.as_view(), name='product_detail'),

]