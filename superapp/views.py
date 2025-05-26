from django.shortcuts import render, redirect, HttpResponseRedirect
from superapp.models import (
    Product,
    OrderItem,
    Order,
    Countries,
    Contact,
    Checkout,
    Customer,
)
import json
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.contrib import auth, messages
from django.contrib.auth.models import User
from .middlewares import check_login


def base(request):
    products_new = Product.objects.filter(new=True)
    context = {"products_new": products_new}

    return render(request, "base.html", context)


def index(request):
    products_sale = Product.objects.filter(sale=True)
    products_sports = Product.objects.filter(sub_category="Sports")

    context = {
        "products_sale": products_sale,
        "products_sports": products_sports,
    }
    print(context["products_sale"])
    print(context["products_sports"])

    return render(request, "index.html", context)


def login(request):
    url = request.GET.get("url")

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)

            if url:
                return HttpResponseRedirect(url)
            else:
                return redirect("login")

        else:
            messages.info(request, "Please Create account first!")
            return redirect("login")

    return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect("login")


def singup(request):
    if request.method == "POST":
        username = request.POST.get("s_username")
        email = request.POST.get("email")
        password = request.POST.get("s_password")
        confirm_password = request.POST.get("c_password")

        if password != confirm_password:
            messages.info(request, "Passwords don't Match!")

        elif User.objects.filter(username=username).exists():
            messages.info(request, "Username Already exits!")
            return "signup"

        elif User.objects.filter(email=email).exists():
            messages.info(request, "Email already exists!")
            return redirect("signup")

        else:
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.save()

            customer = Customer.objects.create(
                user=user, email=email, username=username
            )
            customer.save()

            messages.info(request, "Account Created Successfully!")

            return redirect("login")

    return render(request, "signup.html")


def product_list(request, page=1):
    products = Product.objects.all()
    items = Product.objects.all()
    paginator = Paginator(items, 10)

    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            source = data.get("source")
            newChecked = data["newChecked"]
            saleChecked = data["saleChecked"]
            value1 = data.get("value1")
            value2 = data.get("value2")
            itemsperPage = data.get("itemsPerPage")
            itemsOrder = data.get("itemsOrder")
            searchItem = data.get("searchBox")

            if newChecked and saleChecked:
                products = Product.objects.filter(new=True, sale=True)

            elif newChecked:
                products = Product.objects.filter(new=True)

            elif saleChecked:
                products = Product.objects.filter(sale=True)

            products = products.filter(price__gte=value1, price__lte=value2)

            if itemsOrder.lower() == "name (a - z)":
                products = products.order_by("name")
            elif itemsOrder.lower() == "name (z - a)":
                products = products.order_by("-name")
            elif itemsOrder.lower() == "price (low > high)":
                products = products.order_by("price")
            elif itemsOrder.lower() == "price (high > low)":
                products = products.order_by("-price")

            totalProducts = products

            product_list = []
            if source != "page_filter" and len(searchItem) == 0:
                for product in products:
                    product_list.append(
                        {
                            "id": product.id,
                            "name": product.name,
                            "price": product.price,
                            "image": product.imageURL,
                            "sale": product.sale,
                            "new": product.new,
                        }
                    )

            elif len(searchItem) > 0:
                for product in products:
                    if search(searchItem, product):
                        product_list.append(
                            {
                                "id": product.id,
                                "name": product.name,
                                "price": product.price,
                                "image": product.imageURL,
                                "sale": product.sale,
                                "new": product.new,
                            }
                        )

                totalProducts = product_list

                if source == "page_filter":
                    page_no = data.get("page_no")
                    if len(product_list) > 0:
                        if itemsperPage <= len(product_list):
                            product_list = product_list[
                                itemsperPage * (page_no - 1) : itemsperPage * page_no
                            ]
                        else:
                            product_list = product_list[itemsperPage * (page_no - 1) :]

            elif source == "page_filter":
                page_no = data.get("page_no")

                i = 1
                for product in products:
                    if i <= page_no * itemsperPage and i > (page_no - 1) * itemsperPage:
                        product_list.append(
                            {
                                "id": product.id,
                                "name": product.name,
                                "price": product.price,
                                "image": product.imageURL,
                                "sale": product.sale,
                                "new": product.new,
                            }
                        )
                    i += 1

            if len(product_list) > 0:
                product_list[0]["totalItems"] = len(totalProducts)

            return JsonResponse(product_list, safe=False)

        except Exception as e:
            print(e)

    context = {"products": products, "items": current_page}

    return render(request, "product-list.html", context)


def search_result(request, page=1):
    products = Product.objects.all()
    product_list = []
    message = ""

    if request.method == "POST":
        searchItem = request.POST["searchBox"]

        if len(searchItem) > 3:
            for product in products:
                if search(searchItem, product):
                    product_list.append(
                        {
                            "id": product.id,
                            "name": product.name,
                            "price": product.price,
                            "imageURL": product.imageURL,
                            "sale": product.sale,
                            "new": product.new,
                        }
                    )

            if len(product_list) > 0:
                product_list[0]["totalItems"] = len(product_list)
            message = searchItem

    paginator = Paginator(product_list, 10)  # 10 items per page
    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)

    context = {"products": product_list, "items": current_page, "message": message}
    return render(request, "search-result.html", context)


def item(request, id):
    product = Product.objects.get(id=id)

    item = OrderItem.objects.filter(product=product)
    if item.exists():
        item = item.first()
    else:
        item = 0

    context = {"product": product, "item": item}
    return render(request, "item.html", context)


def shopping_cart(request):
    if request.method == "POST":
        customer = request.user.customer
        try:
            data = json.loads(request.body)
            id = data["id"]
            action = data["action"]
            value = data["value"]
            value = float(value)

            orders = Order.objects.filter(customer=customer, complete=False)

            if orders.exists():
                order = orders.first()
            else:
                order = Order.objects.create(customer=customer, complete=False)

            product = Product.objects.get(id=id)
            items = OrderItem.objects.filter(order=order, product=product)

            if items.exists():
                item = items.first()
                add = False
            else:
                item = OrderItem.objects.create(
                    order=order, product=product, quantity=0
                )
                add = True

            if action == "add":
                item.quantity += 1
            elif action == "remove":
                item.quantity = max(item.quantity - 1, 0)
            elif action == "additems":
                if value == 0:
                    item.quantity = 0
                elif value < item.quantity:
                    item.quantity = value
                else:
                    item.quantity = item.quantity + (value - item.quantity)

            item.save()
            order.save()

            if item.quantity == 0:
                item.delete()
                remove = True
                add = False
            else:
                remove = False

            cart_total_items = order.cart_total_items
            cart_total_price = round(order.cart_total_price, 2)
            quantity = int(item.quantity)
            image = product.imageURL
            name = product.name
            total_price = round(item.total_price, 2)

            mydict = {
                "name": name,
                "image": image,
                "total_price": total_price,
                "quantity": quantity,
                "remove": remove,
                "add": add,
                "cart_total_items": cart_total_items,
                "cart_total_price": cart_total_price,
            }

            return JsonResponse(mydict)

        except Exception as e:
            print(e)
            return JsonResponse("ERROR", safe=False)

    return render(request, "shopping-cart.html")


def kids(request):
    products = Product.objects.filter(category="KIDS")
    item = []
    context = {"products": products, "item": item}
    return render(request, "kids.html", context)


def checkout(request):
    countries = Countries.objects.all()

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            email = data.get("email")
            phone = data.get("phone")
            address = data.get("address")
            postal_code = data["postal_code"]
            city = data.get("city")
            state = data.get("state")
            country = data.get("country")
            comments = data.get("desc", "NO comments")
            cashOnDelivery = data.get("cashOnDelivery")
            total = data.get("total")

            checkout = Checkout.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address,
                postal_code=postal_code,
                state=state,
                city=city,
                country=country,
                comments=comments,
                cashOnDelivery=cashOnDelivery,
            )
            if request.user.is_authenticated:
                customer = request.user.customer

                transaction_id = datetime.now().timestamp()

                order = Order.objects.filter(customer=customer)
                order = order.last()
                order.complete = True
                order.transaction_id = transaction_id

                if order.cart_total_price == total:
                    order.save()
            checkout.save()

            return JsonResponse("data was added!", safe=False)

        except Exception as e:
            print(e)

    context = {"countries": countries}
    return render(request, "checkout.html", context)


def about(request):
    return render(request, "about.html")


def contact(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        desc = request.POST["textarea"]

        contact = Contact.objects.create(name=name, email=email, desc=desc)
        contact.save()
        message = "You form is submitted Successfully!"
        context = {"message": message}
        return render(request, "contact.html", context)

    return render(request, "contact.html")


@check_login
def account(request):
    return render(request, "account.html")


def faq(request):
    return render(request, "faq.html")


def privacy_policy(request):
    return render(request, "privacy-policy.html")


def search(text, product):
    find = False
    text = text.lower()
    if (
        text in product.name.lower()
        or text in product.desc.lower()
        or text in product.category.lower()
        or text in product.sub_category.lower()
    ):
        find = True
    return find


def terms_conditions(request):
    return render(request, "terms-conditions.html")
