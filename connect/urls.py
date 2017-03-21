from django.conf.urls import url, include
from connect import views
import notifications.urls

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^landing/$', views.landing, name='landing'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^about/$', views.about, name='about'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^edit/$', views.user_edit, name='edit'),
    url(r'^users/$', views.users, name='users'),
    url(r'^pos_map/$', views.pos_map, name='pos_map'),
    url(r'^all_users/$', views.all_users, name='all_users'),
    url(r'^uni_news/$', views.uni_news, name='uni_news'),
    url(r'^notifications/', include(notifications.urls, namespace='notifications')),
    url(r'^notification/$', views.notification, name='notification'),
    url(r'^messages/$', views.messages, name='messages'),
]
