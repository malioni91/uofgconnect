from django.conf.urls import url
from connect import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^landing/$', views.landing, name='landing'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^about/$', views.about, name='about'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^contact/$', views.faq, name='contact'),
    url(r'^edit/$', views.user_edit, name='edit'),
]
