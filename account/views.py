from django.shortcuts import render, redirect
from .form import UserRegistration, UserLogin, UserUpdate

# Email Verification
from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer_generate
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User

from django.contrib.auth import authenticate
from django.contrib.auth.models import auth

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from payment.forms import ShippingAddressForm
from payment.models import ShippingAddress, OrderItem




def register(request):

    form = UserRegistration()

    if request.method == 'POST':
        form = UserRegistration(request.POST)

        if form.is_valid():
            user = form.save()

            user.is_active = False

            #Email Verification

            current_site = get_current_site(request)
            subject = f'Account Verification Email - {user.username}'
            message = render_to_string('account/authentication/email_verification/email_verification.html', {

                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user),

            })

            user.email_user(subject=subject, message=message)

            return redirect('email_verification_sent')
            
            
    return render(request, 'account/authentication/register.html', {'form': form})



def email_verification(request, uidb64, token):

    decrypt_uid = force_str(urlsafe_base64_decode(uidb64))

    user = User.objects.get(pk=decrypt_uid)

    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        return redirect('email_verification_success')
    
    user.delete()
    return redirect('email_verification_failed')
    



def email_verification_success(request):
    return render(request, 'account/authentication/email_verification/email_verification_success.html')




def email_verification_sent(request):
    return render(request, 'account/authentication/email_verification/email_verification_sent.html')



def email_verification_failed(request):
    return render(request, 'account/authentication/email_verification/email_verification_failed.html')



def user_login(request):
    form = UserLogin()
    if request.method == 'POST':
        form = UserLogin(request, data=request.POST)

        if form.is_valid():

            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)

            if user:
                auth.login(request, user)
                messages.success(request, "Login success", extra_tags="login")
                return redirect('dashboard')
    
    return render(request, 'account/authentication/user_login.html', {'form': form})
        
@login_required(login_url='user_login')
def user_logout(request):
    session_data = request.session.get('session_key', None)
    current_expiry = request.session.get('_session_expiry')
    auth.logout(request)
    if session_data:
        request.session['session_key'] = session_data
        if current_expiry:
           request.session['_session_expiry'] = current_expiry
    messages.success(request, "Logout success")
    return redirect("store")


@login_required(login_url='user_login')
def dashboard(request):
    return render(request, 'account/dashboard.html')


# Track Order
def track_orders(request):
    pass

@login_required(login_url='user_login')
def profile_update(request):
    form = UserUpdate(instance=request.user)

    if request.method == 'POST':
        form = UserUpdate(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.info(request, "Account updated")
            return redirect('dashboard')
    

    return render(request, 'account/profile_management/profile_update.html', {'form': form})

@login_required(login_url='user_login')
def profile_delete(request):

    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.error(request, "Account deleted")
        return redirect('register')

    return render(request, 'account/profile_management/profile_delete.html')


@login_required(login_url='user_login')
def manage_shipping(request):

    try:
        shipping = ShippingAddress.objects.get(user=request.user.id)
    
    except ShippingAddress.DoesNotExist:
        shipping = None 
    

    shipping_form = ShippingAddressForm(instance=shipping)

    if request.method == 'POST':
        shipping_form = ShippingAddressForm(request.POST, instance=shipping)

        if shipping_form.is_valid():

            shipping_user = shipping_form.save(commit=False)

            shipping_user.user = request.user

            shipping_user.save()

            messages.info(request, f'{shipping_user.user} address updated')

            return redirect('dashboard')
    
    return render(request, 'account/shipping/manage_shipping.html', {'form': shipping_form})



@login_required(login_url='my-login')
def track_orders(request):

    try:

        orders = OrderItem.objects.filter(user=request.user)

        context = {'orders':orders}

        return render(request, 'account/order/track_orders.html', context=context)

    except:

        return render(request, 'account/order/track_orders.html')


