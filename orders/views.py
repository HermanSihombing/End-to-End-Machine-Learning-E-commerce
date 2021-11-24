from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        print("POST")
        form = OrderCreateForm(request.POST)
        print("request POST")
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            cart.clear()
            return render(request, 'orders/order/created.html', {'order':order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})
        # return redirect('/')





