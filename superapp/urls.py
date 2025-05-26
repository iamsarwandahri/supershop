from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="home"),
    path("index/", views.index, name="index"),
    path("base", views.base, name="base"),
    path("index/<int:id>/item/", views.item, name="item"),
    path("kids/", views.kids, name="kids"),
    path("about/", views.about, name="about"),
    path("account/", views.account, name="account"),
    path("checkout/", views.checkout, name="checkout"),
    path("contact/", views.contact, name="contact"),
    path("faq/", views.faq, name="faq"),
    path("privacy_policy/", views.privacy_policy, name="privacy_policy"),
    path("product_list/", views.product_list, name="product_list"),
    path("search_result/", views.search_result, name="search_result"),
    path("shopping_cart/", views.shopping_cart, name="shopping_cart"),
    path("terms_conditions/", views.terms_conditions, name="terms_conditions"),
    path("login/", views.login, name="login"),
    path("signup/", views.singup, name="signup"),
    path("logout/", views.logout, name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
