import contextlib

import requests
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.db.models import Count
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from apps.cart.models import Cart, CartItem
from apps.cart.views import _get_session_id

from .forms import CustomUserCreationForm
from .models import User

# Create your views here.


def signup(request):
    form = CustomUserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()

        mail_subject = "Bienvenido a GreatKart! Activa tu cuenta"
        current_site = get_current_site(request)
        message = render_to_string(
            "accounts/account_verification_email.html",
            {
                "user": user,
                "domain": current_site,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
            },
        )
        send_email = EmailMessage(mail_subject, message, to=[user.email])
        send_email.send()

        return redirect(reverse("accounts:login") + "?command=verification&email=" + user.email)

    context = {"form": form}

    return render(request, "accounts/signup.html", context)


def activate(request, uidb64, token):
    user = None

    with contextlib.suppress(TypeError, ValueError, OverflowError, User.DoesNotExist):
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Tú cuenta ha sido activada!")
        return redirect("accounts:login")
    else:
        messages.error(request, "Enlace de activación inválido")
        return redirect("accounts:signup")


def login(request):
    if request.method == "POST":
        user = auth.authenticate(email=request.POST["email"], password=request.POST["password"])
        if user is not None:
            with contextlib.suppress(ObjectDoesNotExist):
                cart = Cart.objects.get(session_id=_get_session_id(request))
                cart_items = CartItem.objects.filter(cart=cart)

                for cart_item in cart_items:
                    cart_item_variations = list(cart_item.variations.all())
                    try:
                        user_item = (
                            CartItem.objects.filter(
                                user=user, product=cart_item.product, variations__in=cart_item_variations
                            )
                            .annotate(num_variations=Count("variations"))
                            .filter(num_variations=len(cart_item_variations))
                            .get()
                        )
                        user_item.quantity += 1
                        user_item.save()
                    except ObjectDoesNotExist:
                        cart_item.user = user
                        cart_item.save()

            auth.login(request, user)

            with contextlib.suppress(Exception):
                url = request.META.get("HTTP_REFERER")
                query = requests.utils.urlparse(url).query
                params = dict(x.split("=") for x in query.split("&"))
                if "next" in params:
                    return redirect(params["next"])

            return redirect("accounts:profile")
        else:
            messages.error(request, "El email o la contraseña son incorrectos.")
            return redirect("accounts:login")

    return render(request, "accounts/login.html")


@login_required(login_url="accounts:login")
def logout(request):
    auth.logout(request)
    return redirect("core:home")


@login_required(login_url="accounts:login")
def profile(request):
    return render(request, "accounts/profile.html")


def password_reset(request):
    if request.method == "POST":
        email = request.POST["email"]

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            mail_subject = "Cambia tu contraseña"
            current_site = get_current_site(request)
            message = render_to_string(
                "accounts/password_reset_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            send_email = EmailMessage(mail_subject, message, to=[user.email])
            send_email.send()

            messages.success(request, "Restaura la contraseña con el enlace que hemos enviado a tu correo electónico")

            return redirect("accounts:login")

    return render(request, "accounts/password_reset_form.html")


def password_reset_confirm(request, uidb64=None, token=None):
    if request.method == "POST":
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 == password2:
            uid = request.session.get("uid")
            user = User.objects.get(pk=uid)
            user.set_password(password1)
            user.save()
            messages.success(request, "Has restaurado tu contraseña correctamente")
            return redirect("accounts:login")
        else:
            messages.error(request, "Las contraseñas no coinciden")
            return render(request, "accounts/password_reset_confirm.html")

    user = None
    reset_url_token = "set_password"

    if token == reset_url_token:
        session_token = request.session["password_reset_token"]
        with contextlib.suppress(TypeError, ValueError, OverflowError, User.DoesNotExist):
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

        if user is not None and default_token_generator.check_token(user, session_token):
            request.session["uid"] = uid
            messages.success(request, "Ingresa tu nueva contraseña")
            return render(request, "accounts/password_reset_confirm.html")
    else:
        with contextlib.suppress(TypeError, ValueError, OverflowError, User.DoesNotExist):
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

        if user is not None and default_token_generator.check_token(user, token):
            # Store the token in the session and redirect to the password reset form
            # at a URL without the token. That avoids the possibility of leaking the
            # token in the HTTP Referer header.
            request.session["password_reset_token"] = token
            redirect_url = request.path.replace(token, reset_url_token)
            return redirect(redirect_url)
        else:
            messages.error(request, "El enlace ha expirado")

    return redirect("accounts:login")
