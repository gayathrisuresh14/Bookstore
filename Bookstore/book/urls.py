from django.urls import path
from .views import home, about, contact, SearchResult, BookList, BookDetail, BookCheckout, PaymentComplete, cart, add_to_cart, remove_from_cart

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('search/', SearchResult.as_view(), name='search'),
    path('book-list/', BookList.as_view(), name='book_list'),
    path('book-detail/<int:pk>/', BookDetail.as_view(), name='book_detail'),
    path('checkout/<int:pk>/', BookCheckout.as_view(), name='checkout'),
    path('complete/', PaymentComplete, name='complete'),
    path('cart/', cart, name='mycart'),
    path('cart/add/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:book_id>/', remove_from_cart, name='remove_from_cart')

]