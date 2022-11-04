import requests
import decimal
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.conf import settings
from .forms import TransactionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Dashboard, TransactionRecord

User = settings.AUTH_USER_MODEL


@login_required
def dashboard(request):
    user = request.user
    # api for getting the ip accessing our site
    # use the ip to get the city
    url = "http://ip-api.com/json/{}"

    # use city name to get it's weather with
    # weather api below
    weather_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=21e1bce2f7f5badd26f6fba5613cc8c5"

    # Activate in production
    # gets the ip of the user acessing our platform
    # --------------------------------------------------
    # x_forw_for = request.META.get('HTTP_X_FORWARDED_FOR')
    # if x_forw_for is not None:
    # 	ip = x_forw_for.split(',')[0]
    # else:
    # 	ip = request.META.get('REMOTE_ADDR')
    # --------------------------------------------------

    # (Dallas, USA)
    # ip = '69.162.81.155' # hardcoded ip for the development

    # (Prague, Czech)
    # ip = '212.102.39.152'

    # (Lagos, Nigeria)
    ip = "197.210.173.239"

    r = requests.get(url.format(ip)).json()

    get_ips_weather = requests.get(weather_url.format(r["city"])).json()

    user_dashboard = Dashboard.objects.get(user=user)

    context = {
        "city": get_ips_weather["name"],
        "country": r["country"],
        "temperature": get_ips_weather["main"]["temp"],
        "icon": get_ips_weather["weather"][0]["icon"],
        "user_dashboard": user_dashboard,
        "user": user,
    }
    return render(request, "dashboard.html", context)


@login_required
def transfer(request):
    url = "http://ip-api.com/json/{}"

    # # use city name to get it's weather with
    # # weather api below
    weather_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=21e1bce2f7f5badd26f6fba5613cc8c5"

    # # Activate in production
    # # gets the ip of the user acessing our platform
    # # --------------------------------------------------
    # # x_forw_for = request.META.get('HTTP_X_FORWARDED_FOR')
    # # if x_forw_for is not None:
    # # 	ip = x_forw_for.split(',')[0]
    # # else:
    # # 	ip = request.META.get('REMOTE_ADDR')
    # # --------------------------------------------------

    # # (Dallas, USA)
    # #ip = '69.162.81.155' # hardcoded ip for the development

    # #(Prague, Czech)
    ip = "212.102.39.152"
    r = requests.get(url.format(ip)).json()

    get_ips_weather = requests.get(weather_url.format(r["city"])).json()
    # print(get_ips_weather)
    # print(r)
    context = {
        "city": get_ips_weather["name"],
        "country": r["country"],
        "temperature": get_ips_weather["main"]["temp"],
        "icon": get_ips_weather["weather"][0]["icon"],
    }
    return render(request, "transfer.html", context)


@login_required
def create_transaction(request):
    if request.method == "POST":
        get_receiver_tag = request.POST["receiver-wallet-tag"]
        try:
            receiver_with_tag = Dashboard.objects.get(wallet_tag=get_receiver_tag)
        except Dashboard.DoesNotExist:
            return HttpResponse("Invalid  wallet tag")
        receiver = receiver_with_tag.user
        sender = Dashboard.objects.get(user=request.user)
        amount = request.POST["amount"]
        # print(sender.wallet_balance)
        # print(receiver_with_tag.wallet_balance)
        if sender.wallet_balance > int(amount):
            sender.wallet_balance -= int(amount)
            sender.save()
            receiver_with_tag.wallet_balance += int(amount)
            receiver_with_tag.save()
            new_transaction = TransactionRecord.objects.create(
                sender=sender.user,
                receiver=receiver,
                amount=str(amount),
                transaction_remark="created",
            )
            new_transaction.save()
            print("new transaction record created!")
            return redirect("transactions")
        else:
            return HttpResponse("Insufficient Balance")
    return render(request, "transfer.html")


@login_required
def get_all_transactions(request):
    url = "http://ip-api.com/json/{}"
    user = request.user
    # use city name to get it's weather with
    # weather api below
    weather_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=21e1bce2f7f5badd26f6fba5613cc8c5"

    # Activate in production
    # gets the ip of the user acessing our platform
    # --------------------------------------------------
    # x_forw_for = request.META.get('HTTP_X_FORWARDED_FOR')
    # if x_forw_for is not None:
    # 	ip = x_forw_for.split(',')[0]
    # else:
    # 	ip = request.META.get('REMOTE_ADDR')
    # --------------------------------------------------

    # (Dallas, USA)
    ip = "69.162.81.155"  # hardcoded ip for the development

    # (Prague, Czech)
    # ip = '212.102.39.152'

    # (Lagos, Nigeria)
    # ip = '197.210.173.239'

    r = requests.get(url.format(ip)).json()

    get_ips_weather = requests.get(weather_url.format(r["city"])).json()
    # print(get_ips_weather)
    # print(r)
    all_transactions = TransactionRecord.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).order_by("-timestamp")
    context = {
        "city": get_ips_weather["name"],
        "country": r["country"],
        "temperature": get_ips_weather["main"]["temp"],
        "icon": get_ips_weather["weather"][0]["icon"],
        "all_transactions": all_transactions,
    }

    return render(request, "transactions.html", context)
