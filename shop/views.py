from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Reviewed
from cart.forms import CartAddProductForm
from cart.cart import Cart
from .forms import ReviewedForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    cart = Cart(request)
    count = 0
    for item in cart:
        count += item['quantity']


    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'count':count,
    }
    return render(request, 'shop/product/list.html', context)

@login_required
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    reviewed_product = Reviewed.objects.filter(product=product)

    new_reviewed = None
    cart = Cart(request)
    count = 0
    for item in cart:
        count += item['quantity']

    if request.method == 'POST':
        reviewed_form = ReviewedForm(request.POST)
        if reviewed_form.is_valid():
            reviewed_form = Reviewed()
            # user = User.objects.get()
            reviewed_form.nama = request.user
            reviewed_form.product = product
            reviewed_form.rating = request.POST['rating']
            reviewed_form.comment = request.POST['comment']
            print(reviewed_form.rating, reviewed_form.comment, product, reviewed_form.nama)
            reviewed_form.save()
    else:
        reviewed_form = ReviewedForm()

    context = {
        'product': product,
        'cart_product_form': cart_product_form,
        'reviewed_product':reviewed_product,
        'new_reviewed':new_reviewed,
        'reviewed_form':reviewed_form,
        'count':count,
    }


    return render(request, 'shop/product/detail.html', context)
