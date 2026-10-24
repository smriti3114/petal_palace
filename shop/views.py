import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, LoginForm
from .models import Category, Product,CartItem,Order
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request,'home.html')
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')
def shop(request):
    category= Category.objects.all()
    
    categoryID= request.GET.get('category')
    if categoryID:
        product= Product.objects.filter(category= categoryID)
    else:
        product= Product.objects.all()
    context={
        'category':category,
        'product':product,
    }
    return render(request,'shop.html',context)


def cart(request):
	if request.user.is_authenticated:
		cart_items = CartItem.objects.filter(user=request.user)
		total_price = sum(int(item.product.price) * item.quantity for item in cart_items)
		total_price=int(total_price)
		return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})
	else:
		return redirect('/login')


def add_to_cart(request, id):
	if request.user.is_authenticated:
		product = Product.objects.get(id=id)
		cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
		cart_item.quantity += 1
		cart_item.save()
		return redirect('/shop/')
	else:
		return redirect('/login/')
     
def user_login(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # ✅ IMPORTANT FIX
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid email or password')

    return render(request, 'login.html', {'form': form})

def signup(request):
    form=RegistrationForm(request.POST or None)
    if request.method=="POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully!")

            return redirect('login')
    return render(request, 'signup.html', {'form':form})


def user_logout(request):
    logout(request)
    return redirect('login')

def update_cart(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "Cart updated successfully.")
    return redirect('/cart/')  # 'cart' is the name of the cart view

@login_required
def delete_cart_item(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
    return redirect('/cart/')




def initiate_payment(request):
    if request.method == "POST":
        amount = int(request.POST["amount"]) * 100  # convert to paise
        address = request.POST.get("address")

        # Save address temporarily in session
        request.session['address'] = address

        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

        order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "receipt": "order_receipt"
        })

        return JsonResponse({
            "id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
            "key": settings.RAZORPAY_API_KEY,
            "name": "Petal Palace",
            "description": "Payment for your order"
        })
# def payment_success(request):
#     return render(request, "payment_success")



def payment_success(request):

    cart_items = CartItem.objects.filter(user=request.user)
    address = request.session.get('address')

    for cart in cart_items:
        Order.objects.create(
            user=request.user,
            product=cart.product,
            quantity=cart.quantity,
            payment_status='success',
            address=address
        )

    cart_items.delete()

    messages.success(request, "Payment Successful! Your order has been placed.")

    return redirect('/')