from django.db import transaction
from django.forms import inlineformset_factory

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from basketapp.models import Basket
from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItem


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderItemCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:order_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormset = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.method == 'POST':
            formset = OrderFormset(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if basket_items.exists():
                OrderFormset = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=basket_items.count())
                formset = OrderFormset()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                # basket_items.delete()
            else:
                formset = OrderFormset()
        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            Basket.objects.filter(user=self.request.user).delete()
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        return super().form_valid(form)


class OrderItemUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:order_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormset = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.method == 'POST':
            formset = OrderFormset(self.request.POST, instance=self.object)
        else:
            formset = OrderFormset(instance=self.object)
        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        return super().form_valid(form)


class OrderItemDetail(DetailView):
    model = Order


class OrderItemDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:order_list')
