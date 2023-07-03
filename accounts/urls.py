from django.urls import include, re_path
#from django.contrib.auth.views import logout

from accounts import views


urlpatterns = [
    re_path(r'^send_login_email$', views.send_login_email, name='send_login_email'),
#    re_path(r'^lists/', include(list_urls)),
#    re_path(r'^accounts/', include(accounts_urls)),
]
