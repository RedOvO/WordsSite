from django.conf.urls import url, include
from myapp import views

urlpatterns = [
    url(r'login$', views.login2),
    url(r'signup$', views.signup),
    url(r'logout', views.logout2),
    url(r'recite/cet4$', views.recite_cet4),
    url(r'recite/cet6$', views.recite_cet6),
    url(r'recite/cet4_next', views.cet4_next),
    url(r'recite/cet6_next', views.cet6_next),
    url(r'recite/collect', views.collect),
    url(r'wordsbook/delete', views.delete),
    url(r'wordsbook/cet4_list', views.cet4_list),
    url(r'wordsbook/cet6_list', views.cet6_list),
    url(r'review/cet4_review', views.cet4_review_test),
    url(r'review/cet6_review', views.cet6_review_test),
    url(r'test/cet4_test', views.cet4_review_test),
    url(r'test/cet6_test', views.cet6_review_test),
    url(r'setting/plan', views.setting),
]
