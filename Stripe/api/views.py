import os

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, TemplateView, View
from dotenv import load_dotenv
import stripe

from .forms import OrderForm
from .models import Item, Order

load_dotenv()


stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

customer = stripe.Customer.create()
products = stripe.Product.list()
prices = stripe.Price.list()


domain_url = os.getenv('DOMAIN_URL')


class AllItemsView(ListView):
    """Вывод списка товаров."""
    model = Item
    template_name = 'index.html'
    context_object_name = 'items'
    paginate_by = 4

    def get_queryset(self):
        """Экспорт из Stripe в БД Django."""
        for prod in products:
            price_ = [x for x in prices.data if x.product == prod.id][0]
            price = float(price_.unit_amount / 100)
            obj, created = Item.objects.get_or_create(name=prod.name)
            if created:
                obj.description = prod.description or ''
                obj.price = price
                obj.save()
        return Item.objects.all()


class OrderListView(ListView):
    """Детальный просмотр заказов."""
    model = Order
    template_name = 'order_list.html'
    context_object_name = 'orders'
    paginate_by = 4


class ItemView(DetailView):
    """Детальный просмотр товара."""
    model = Item
    template_name = 'item_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_pub_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


class ItemBuyView(View):
    """Создание сессии с Stripe для обработки покупки выбранного товара."""

    def get(self, request, *args, **kwargs):
        item_id = self.kwargs['pk']
        item = Item.objects.get(pk=item_id)
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success/',
                cancel_url=domain_url + 'cancel/',
                mode='payment',
                line_items=[{
                    'price_data': {
                        'currency': item.currency,
                        'product_data': {
                            'name': item.name,
                        },
                        'unit_amount': int(item.price * 100),
                    },
                    'quantity': 1,
                }],
            )
        except Exception as e:
            return JsonResponse({'error': str(e)})
        return JsonResponse({'sessionId': checkout_session['id']})


class SuccessPayView(TemplateView):
    """Информация об успешной покупке."""
    template_name = 'success.html'


class CancelPayView(TemplateView):
    """Информация об отказе от покупки."""
    template_name = 'cancel.html'


def add_to_order(request):
    """Форма создания заказа."""
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            order_items = order.items.all()
            order.total_price = sum(item.price for item in order_items)
            order.save()
            return redirect('orders_list')
    else:
        form = OrderForm()
    return render(request, 'add_to_order.html', {'form': form})


class OrderPaymentView(TemplateView):
    """Страница оплаты заказа."""
    template_name = 'order_detail.html'

    def get_context_data(self, **kwargs):
        order_id = self.kwargs['pk']
        order = Order.objects.get(id=order_id)
        items = order.items.all()
        stripe_pub_key = settings.STRIPE_PUBLISHABLE_KEY
        context = super().get_context_data(**kwargs)
        context.update({
            'items': items,
            'order': order,
            'clientSecret': stripe_pub_key,
            'stripe_pub_key': stripe_pub_key,
            'domain_url': domain_url,
        })
        return context


class StripeIntentView(View):
    """Загрузка формы оплаты на страницу."""

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            try:
                order_id = self.kwargs['pk']
                order = Order.objects.get(id=order_id)
                intent = stripe.PaymentIntent.create(
                    amount=int(order.get_total_price * 100),
                    currency='rub',
                    automatic_payment_methods={
                        'enabled': True,
                    },
                    customer=customer['id'],
                    metadata={
                        'order_id': order.id,
                    },
                )
                return JsonResponse({
                    'clientSecret': intent['client_secret'],
                })
            except Exception as e:
                return JsonResponse({'error': str(e)})


def error_404(request, exception):
    template = '404.html'
    return render(request, template, status=404)


def error_500(request):
    template = '500.html'
    return render(request, template, status=500)
