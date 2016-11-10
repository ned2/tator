from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import AnnotateView, welcome, instructions, index


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^annotate/$', AnnotateView.as_view(), name='annotate'),
    url(r'^welcome/$', welcome, name='welcome'),
    url(r'^instructions/$', instructions, name='instructions'),
    url(r'^logout/$', auth_views.logout_then_login, name='logout'),
    url(r'^login/$', auth_views.login, {'template_name': 'annotate/login.html'}, name='login'),
]
