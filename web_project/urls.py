"""web_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from web_project import views
from web_project import customers
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.home, name="home"),
    path("get", views.get, name="get"),
    path("post", views.post, name="post"),
    path("displayOrder", views.displayOrder, name="displayOrder"),
    path("getCustomers", customers.getCustomers, name="getCustomers"),
    path("manageCustomers", customers.manageCustomers, name="manageCustomers"),
    path("addCustomer", customers.addCustomer, name="addCustomer"),
    path("manageCustomersWithValidation", customers.manageCustomersWithValidation, name="manageCustomersWithValidation")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
