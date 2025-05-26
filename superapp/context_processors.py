from .models import Product, Order, OrderItem


def common_data(request):
    all_products = Product.objects.all()
    products_new = Product.objects.filter(new=True)

    if request.user.is_authenticated:
        customer = request.user.customer

        orders = Order.objects.filter(customer=customer, complete=False)

        if orders.exists():
            order = orders.first()
        else:
            order = Order.objects.create(customer=customer, complete=False)

        items = OrderItem.objects.filter(order=order)

        cart_total_items = int(order.cart_total_items)
        cart_total_price = order.cart_total_price

        context = {
            "c_total_items": cart_total_items,
            "c_total_price": cart_total_price,
            "all_products": all_products,
            "c_items": items,
            "products_new": products_new,
        }

    else:
        context = {
            "c_total_items": 0,
            "c_total_price": 0,
            "all_products": all_products,
            "c_items": [],
            "products_new": products_new,
        }

    return context
