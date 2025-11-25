from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),  # ← главная
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="beer/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path("add_days/<int:days>/", views.add_days, name="add_days"),
    path('shop/', views.shop, name='shop'),
    path('add_days/<int:days>/', views.add_days, name='add_days'),
    path('brew/', views.brew, name='brew'),
    path('start_brew/<int:recipe_id>/', views.start_brew, name='start_brew'),
    path('current/', views.current_brews, name='current'),
    path("inventory/", views.inventory, name="inventory"),
    path("shop/hops/", views.shop_hops, name="shop_hops"),
    path("shop/malts/", views.shop_malts, name="shop_malts"),
    path("shop/yeasts/", views.shop_yeasts, name="shop_yeasts"),
    path("shop/mills/", views.shop_mills, name="shop_mills"),
    path("shop/containers/", views.shop_containers, name="shop_containers"),
    path("shop/brewers/", views.shop_brewers, name="shop_brewers"),
    path("shop/tanks/", views.shop_tanks, name="shop_tanks"),
    path("shop/hops/<int:hop_id>/", views.hop_detail, name="hop_detail"),
    path("shop/malts/<int:malt_id>/", views.malt_detail, name="malt_detail"),
    path("shop/yeasts/<int:yeast_id>/", views.yeast_detail, name="yeast_detail"),
]
