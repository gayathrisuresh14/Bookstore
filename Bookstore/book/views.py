from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from .models import Book, Order, Cart, CartItems, Contact
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        if len(name) < 3 or len(email) < 4 or len(message) < 3:
            messages.error(request, "Please enter the details correctly")
        else:
            contact = Contact(name=name, email=email, message=message)
            contact.save()
            messages.success(request, "Message sent successfully")

    return render(request, 'contact.html')

class SearchResult(ListView):
    model = Book
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(
            Q(title=query) | Q(author=query)
        )


class BookList(ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'booklist.html'

class BookDetail(DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'bookdetail.html'

class BookCheckout(DetailView):
    model = Book
    template_name = 'checkout.html'


def PaymentComplete(request, pk):
    product = Book.objects.get(id=pk)
    Order.objects.create(product=product)
    return JsonResponse('Payment Completed', safe=False)

@login_required
def cart(request):
    cart_qs = Cart.objects.filter(user=request.user)
    if cart_qs.exists():
        cart_obj = cart_qs.first()
        cart_item = CartItems.objects.filter(cart=cart_obj)
        total_quantity = sum(item.quantity for item in cart_item)
        total_price = sum(item.get_total_price() for item in cart_item)
    else:
        cart_obj = None
        cart_item = []
        total_quantity = 0
        total_price = 0

    context = {
        'cart': cart_obj,
        'cart_items': cart_item,
        'total_quantity': total_quantity,
        'total_price': total_price
    }

    return render(request, 'mycart.html', context)


@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart_qs = Cart.objects.filter(user=request.user)
    if cart_qs.exists():
        cart_obj = cart_qs.first()
    else:
        cart_obj = Cart.objects.create(user=request.user, total_price=Decimal('0.00'))
    cart_item, created = CartItems.objects.get_or_create(book=book, cart=cart_obj)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    cart_obj.total_price += Decimal(str(book.price))
    cart_obj.save()
    return redirect('mycart')


@login_required
def remove_from_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart_qs = Cart.objects.filter(user=request.user)
    if cart_qs.exists():
        cart_obj = cart_qs.first()
        cart_item_qs = CartItems.objects.filter(book=book, cart=cart_obj)
        if cart_item_qs.exists():
            cart_item = cart_item_qs.first()
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        cart_obj.total_price -= Decimal(str(book.price))
        cart_obj.save()
        return redirect('mycart')