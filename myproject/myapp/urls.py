from django.conf.urls import url, include
from myapp import views

urlpatterns = [
    url(r'login$', views.login2),
    url(r'signup$', views.signup),
    url(r'recite/cet4$', views.cet4),
    url(r'recite/cet6$', views.cet6),
]
