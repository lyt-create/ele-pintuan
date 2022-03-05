"""ele URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from ele import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.order),
    path('order.html', views.order),
    path('cook.html', views.cook),
    path('me.html', views.me),
    path('login.html', views.login),
    path('logout.html', views.logout),
    path('register.html', views.register),
    path('orderdata.html', views.orderdata),
    path('mydata.html', views.mydata),
    path('myorder.html', views.myorder),
    path('cookset.html', views.cookset),
    path('start.html', views.start),
    path('createmodel.html', views.createmodel),
    path('join.html', views.join),
    path('modelset.html', views.modelset),
    path('modelchange.html', views.modelchange),
    path('success.html', views.success),
    path('error.html', views.error),
    path('alllist.html', views.alllist),
    path('tuanlist.html', views.tuanlist),
    path("look.html", views.look),
    path("deal.html", views.deal),
    path("del.html", views.delit),


]
