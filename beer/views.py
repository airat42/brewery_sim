from django.shortcuts import render, redirect, get_object_or_404
from .models import Hop, Malt, Yeast, Recipe, Beer, GameState, HopInventory, MaltInventory, YeastInventory, Brewer, Mill
from .models import Container, Tank, BrewerInventory
from django.db import models
from datetime import timedelta
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def get_state(user):
    """
    Возвращает объект состояния для конкретного пользователя.
    """
    state, created = GameState.objects.get_or_create(
        user=user,
        defaults={'current_date': '2025-01-01', 'money': 5000}
    )
    return state

@login_required
def home(request):
    state = get_state(request.user)

    # Получаем BrewerInventory пользователя с максимальным volume
    top_brewer = BrewerInventory.objects.filter(user=request.user).order_by('-brewer__volume').first()

    # Если инвентаря нет, можно оставить дефолтное изображение
    if top_brewer:
        brewer_image = top_brewer.brewer.img
    else:
        brewer_image = "https://i.imgur.com/KTj8q7B.jpeg"  # дефолтное

    return render(request, "beer/home.html", {
        "state": state,
        "brewer_image": brewer_image
    })

# def home(request):
#     state = GameState.objects.first()
#     if not state:
#         state = GameState.objects.create(current_date="2023-01-01")
#
#     return render(request, "beer/home.html", {"state": state})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "beer/register.html", {"form": form})

def shop(request):
    hops = Hop.objects.all()
    malts = Malt.objects.all()
    yeasts = Yeast.objects.all()
    state = get_state(user=request.user)
    return render(request, 'beer/shop.html', {'hops':hops,'malts':malts,'yeasts':yeasts,'state':state})

def add_days(request, days):
    days = int(days)
    state = get_state(user=request.user)
    state.current_date += timedelta(days=days)
    state.save()

    decay_ingredients(days)

    return redirect('home')

def decay_ingredients(days):
    # Хмель
    for item in HopInventory.objects.all():
        item.freshness = max(item.freshness - days, 0)
        if item.freshness == 0:
            item.delete()
        else:
            item.save()

    # Солод
    for item in MaltInventory.objects.all():
        item.freshness = max(item.freshness - days, 0)
        if item.freshness == 0:
            item.delete()
        else:
            item.save()

    # Дрожжи
    for item in YeastInventory.objects.all():
        item.freshness = max(item.freshness - days, 0)
        if item.freshness == 0:
            item.delete()
        else:
            item.save()

def brew(request):
    recipes = Recipe.objects.all()
    return render(request, 'beer/brew.html', {'recipes':recipes})

def start_brew(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    Beer.objects.create(recipe=recipe, volume=100, status='mash')
    return redirect('brew')

def current_brews(request):
    beers = Beer.objects.all()
    return render(request, 'beer/current.html', {'beers':beers})

def shop_hops(request):
    items = Hop.objects.all()
    return render(request, "beer/shop_hops.html", {"items": items})

def shop_malts(request):
    items = Malt.objects.all()
    return render(request, "beer/shop_malts.html", {"items": items})

def shop_yeasts(request):
    items = Yeast.objects.all()
    return render(request, "beer/shop_yeasts.html", {"items": items})

@login_required
def shop_brewers(request):
    items = Brewer.objects.all()
    state = get_state(request.user)

    if request.method == "POST":
        brewer_id = int(request.POST.get("brewer_id"))
        brewer = get_object_or_404(Brewer, id=brewer_id)

        if state.money < brewer.price:
            return HttpResponse("Недостаточно денег!")

        state.money -= brewer.price
        state.save()

        inv, created = BrewerInventory.objects.get_or_create(
            user=request.user,
            brewer=brewer,
            defaults={"quantity": 1}
        )
        if not created:
            inv.quantity += 1
            inv.save()

        return redirect("shop_brewers")

    return render(request, "beer/shop_brewers.html", {"items": items})

def shop_mills(request):
    items = Mill.objects.all()
    return render(request, "beer/shop_mills.html", {"items": items})

def shop_tanks(request):
    items = Tank.objects.all()
    return render(request, "beer/shop_tanks.html", {"items": items})

def shop_containers(request):
    items = Container.objects.all()
    return render(request, "beer/shop_containers.html", {"items": items})

def inventory(request):
    hops_inv = HopInventory.objects.select_related("hop")
    malts_inv = MaltInventory.objects.select_related("malt")
    yeasts_inv = YeastInventory.objects.select_related("yeast")

    return render(
        request,
        "beer/inventory.html",
        {
            "hops_inv": hops_inv,
            "malts_inv": malts_inv,
            "yeasts_inv": yeasts_inv,
        }
    )

# Хмель
@login_required
def hop_detail(request, hop_id):
    hop = get_object_or_404(Hop, id=hop_id)
    quantities = [50, 100, 200, 1000, 5000]

    # список кортежей: (кол-во, общая цена)
    quantity_prices = [(q, get_hops_discounted_price(hop.price, q) * q) for q in quantities]

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        unit_price = get_hops_discounted_price(hop.price, quantity)
        total_price = unit_price * quantity

        # получаем состояние пользователя (деньги)
        state = get_state(user=request.user)
        if state.money < total_price:
            return HttpResponse("Недостаточно денег!")

        state.money -= total_price
        state.save()

        # создаём или обновляем инвентарь
        entry, created = HopInventory.objects.get_or_create(
            user=request.user,
            hop=hop,
            defaults={"quantity": quantity, "freshness": 100}
        )
        if not created:
            entry.quantity += quantity
            entry.freshness = 100  # можно обновлять свежесть до 100 при покупке
            entry.save()

        return redirect("inventory")

    return render(request, "beer/hop_detail.html", {
        "hop": hop,
        "quantity_prices": quantity_prices,
    })

# Солод
@login_required
def malt_detail(request, malt_id):
    malt = get_object_or_404(Malt, id=malt_id)
    quantities = [1, 5, 25, 50, 100, 500]

    # создаём список кортежей: (кол-во, цена за штуку)
    quantity_prices = [(q, get_malt_discounted_price(malt.price, q) * q) for q in quantities]

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        unit_price = get_malt_discounted_price(malt.price, quantity)
        total_price = unit_price * quantity

        state = get_state(user=request.user)
        if state.money < total_price:
            return HttpResponse("Недостаточно денег!")

        state.money -= total_price
        state.save()

        entry, created = MaltInventory.objects.get_or_create(
            user=request.user,
            malt=malt,
            defaults={"quantity": quantity, "freshness": 100}
        )
        if not created:
            entry.quantity += quantity
            entry.freshness = 100
            entry.save()

        return redirect("inventory")

    return render(request, "beer/malt_detail.html", {
        "malt": malt,
        "quantity_prices": quantity_prices,
    })


# Дрожжи
@login_required
def yeast_detail(request, yeast_id):
    yeast = get_object_or_404(Yeast, id=yeast_id)
    quantities = [10, 30, 200, 500, 1000]

    # создаём список кортежей: (кол-во, цена за штуку)
    quantity_prices = [(q, get_yeast_discounted_price(yeast.price, q) * q) for q in quantities]

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        unit_price = get_yeast_discounted_price(yeast.price, quantity)
        total_price = unit_price * quantity

        state = get_state(user=request.user)
        if state.money < total_price:
            return HttpResponse("Недостаточно денег!")

        state.money -= total_price
        state.save()

        entry, created = YeastInventory.objects.get_or_create(
            user=request.user,
            yeast=yeast,
            defaults={"quantity": quantity, "freshness": 100}
        )
        if not created:
            entry.quantity += quantity
            entry.freshness = 100
            entry.save()

        return redirect("inventory")

    return render(request, "beer/yeast_detail.html", {
        "yeast": yeast,
        "quantity_prices": quantity_prices,
    })


def get_malt_discounted_price(base_price, quantity):
    """
    Скидка за объем: чем больше quantity, тем меньше цена за единицу
    Пример:
    1 кг -> 100%
    5 кг -> 95%
    25 кг -> 90%
    50 кг -> 80%
    100 кг -> 70%
    500 кг -> 65%
    """
    if quantity >= 500:
        return base_price * 0.45
    elif quantity >= 100:
        return base_price * 0.55
    elif quantity >= 50:
        return base_price * 0.65
    elif quantity >= 25:
        return base_price * 0.75
    elif quantity >= 5:
        return base_price * 0.85
    else:
        return base_price

def get_hops_discounted_price(base_price, quantity):
    """
    Скидка за объем: чем больше quantity, тем меньше цена за единицу
    Пример:
    50 г -> 100%
    100 г -> 95%
    200 г -> 90%
    1000 г -> 80%
    5000 г -> 70%
    """

    if quantity >= 5000:
        return base_price * 0.7
    elif quantity >= 1000:
        return base_price * 0.8
    elif quantity >= 200:
        return base_price * 0.9
    elif quantity >= 100:
        return base_price * 0.95
    else:
        return base_price


def get_yeast_discounted_price(base_price, quantity):
    """
    Скидка за объем: чем больше quantity, тем меньше цена за единицу
    Пример:
    10 г -> 100%
    30 г -> 95%
    200 г -> 90%
    500 г -> 80%
    1000 г -> 70%
    """

    if quantity >= 1000:
        return base_price * 0.7
    elif quantity >= 500:
        return base_price * 0.8
    elif quantity >= 200:
        return base_price * 0.9
    elif quantity >= 30:
        return base_price * 0.95
    else:
        return base_price