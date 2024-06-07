
from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Product, Order, OrderItem, ShippingAddress, Customer
from django.db import transaction
from django.core.exceptions import MultipleObjectsReturned
import datetime
from . utils import cookieCart, cartData, guestOrder

# Helper function to get or create an order
def get_or_create_order(customer):
    try:
        return Order.objects.get_or_create(customer=customer, complete=False)
    except MultipleObjectsReturned:
        orders = Order.objects.filter(customer=customer, complete=False)
        order = orders.first()
        if orders.count() > 1:
            orders.exclude(id=order.id).delete()  # Optional: clean up extra orders
        return order, False

# Create your views here.
def store(request):
        data = cartData(request)

        cart_items = data['cart_items']
        order = data['order']
        items = data['items']

        products = Product.objects.all()
        context = {'products': products, 'cart_items': cart_items}
        return render(request, 'store/store.html', context)

def cart(request):
        data = cartData(request)

        cart_items = data['cart_items']
        order = data['order']
        items = data['items']

        context = {'items': items, 'order': order, 'cart_items': cart_items}
        return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)

    cart_items = data['cart_items']
    order = data['order']
    items = data['items']


    context = {'items': items, 'order': order, 'cart_items': cart_items}
    return render(request, 'store/checkout.html', context)

@transaction.atomic
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('ProductId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = get_or_create_order(customer)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()


    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)


    else:
        customer, order = guestOrder(request, data)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode']
        )


    return JsonResponse('Payment complete', safe=False)
