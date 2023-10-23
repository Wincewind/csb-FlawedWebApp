"""
URL configuration for flawedsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib.auth.views import LoginView, LogoutView

from .views import index, signup, secret, recovery_init, recovery_attempt, change_pw, email_recovery

insecure_design_fix = False

urlpatterns = [
    path('', index, name='index'),
	path('login/', LoginView.as_view(template_name='pages/login.html')),
	path('logout', LogoutView.as_view(next_page='/')),
	path('signup', signup, name='signup'),
	path('secret/<int:uid>', secret, name='secret'),
    path("admin/", admin.site.urls),
]

if insecure_design_fix:
    urlpatterns.append(path('recovery_init', email_recovery, name='email_recovery'))
else:
    urlpatterns.extend(
        [
        path('recovery_init', recovery_init, name='recovery_init'),
        path('recovery_attempt', recovery_attempt, name='recovery_attempt'),
        path('change_pw', change_pw, name='change_pw'),
    ]
    )
