import json
from .models import Product


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass

    return {'order': order, 'items': items, 'cartItems': cartItems}




def cartData(request):
    try:
        cookieData = json.loads(request.COOKIES.get('cart', '{}'))
    except json.JSONDecodeError:
        cookieData = {}

    try:
        cart_items = cookieData['cart_items']
    except KeyError:
        cart_items = []

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cart_items_count = order['get_cart_items']

    for i in cart_items:
        try:
            cart_items_count += cart_items[i]['quantity']
            product = Product.objects.get(id=i)
            total = (product.price * cart_items[i]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart_items[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart_items[i]['quantity'],
                'get_total': total,
            }
            items.append(item)
        except Product.DoesNotExist:
            pass

    return {
        'cart_items': cart_items,
        'order': order,
        'items': items
    }

def guestOrder(request, data):
    print('User is not logged in...')

    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email = email,
    )
    customer.name = name
    customer.save()

    order = order.objects.create(
        customer = customer,
        complete = False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])


    orderItem = OrderItem.objects.create(
        product = product,
        order = order,
        quantity = item['quantity'],
    )

    return customer, order