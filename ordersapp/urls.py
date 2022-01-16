from django.urls import path

from ordersapp import views as orders

app_name = 'ordersapp'


urlpatterns = [
    path('', orders.OrderList.as_view(), name='order_list'),
    path('create/', orders.OrderItemCreate.as_view(), name='order_create'),
    path('read/<int:pk>/', orders.OrderItemDetail.as_view(), name='order_read'),
    path('update/<int:pk>/', orders.OrderItemUpdate.as_view(), name='order_update'),
    path('delete/<int:pk>/', orders.OrderItemDelete.as_view(), name='order_delete'),
    path('forming/complete/<int:pk>', orders.order_forming_complete, name='order_forming_complete'),

    path('product/<int:pk>/price/', orders.product_price),
]