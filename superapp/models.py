from django.db import models
from django.contrib.auth.models import User
import uuid


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.username


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=264)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    new = models.BooleanField(default=False)
    sale = models.BooleanField(default=False)
    avail = models.BooleanField(default=True)
    desc = models.TextField(
        default="""Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                            Praesent sit amet aliquam elit, sed ornare arcu. Nam gravida pellentesque
                            posuere. Sed sed metus in metus ullamcorper pellentesque. Maecenas tincidunt
                            mi aliquam urna consectetur vulputate. Nullam sed dolor justo."""
    )

    def generate_unique_code():
        unique_code = str(uuid.uuid4().hex)[
            :8
        ]  # Use the first 8 characters of the hexadecimal UUID
        return unique_code

    reference = models.CharField(max_length=100, default=str(generate_unique_code()))
    cat_choices = [
        ("MAN", "MAN"),
        ("WOMAN", "WOMAN"),
        ("KIDS", "KIDS"),
        ("OTHER", "OTHER"),
    ]

    category = models.CharField(choices=cat_choices, max_length=50)
    sub_choices = [
        ("Footwear", "Footwear"),
        ("Clothes", "Clothes"),
        ("Accessories", "Accessories"),
        ("Clearance", "Clearance"),
        ("Technology", "Technology"),
        ("Sports", "Sports"),
        ("Toy", "Toy"),
    ]
    sub_category = models.CharField(choices=sub_choices, max_length=50)
    image = models.ImageField(upload_to="product_images", blank=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except Exception as e:
            print(e)
            url = ""

        return url

    @property
    def quantity(self):
        item = OrderItem.objects.get(product=self)
        return int(item.quantity)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    update = models.CharField(max_length=1000, default="Order Pending!")
    complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.order_id)

    @property
    def cart_total_items(self):
        total = 0
        orderitems = self.orderitem_set.all()
        for item in orderitems:
            total = total + item.quantity
        return int(total)

    @property
    def cart_total_price(self):
        total = 0.0
        orderItems = self.orderitem_set.all()
        for item in orderItems:
            total = total + (float(item.product.price) * item.quantity)
        return round(total, 2)


class OrderItem(models.Model):
    items_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} : {int(self.quantity)}"

    @property
    def total_price(self):
        total = self.quantity * float(self.product.price)
        return round(total, 2)


class Checkout(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=50)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    comments = models.TextField(blank=True)
    cashOnDelivery = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    desc = models.TextField()

    def __str__(self):
        return self.name


class Countries(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
