from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
#from restapi_demo.apidemo import views
from apidemo import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index,name='index'),
    path('rest_register/', views.Signup,name='rest_register'),  # Registration using REST.
    path('rest_login/', views.LoginView.as_view(),name='rest_login'),       # REST Login.
    path('dash/',include('rest_framework.urls', namespace='rest_framework')),

    path('user_login/', views.demo_user_login,name='user_login'),


    url(r'^signup/$', views.Signup, name='signup'),
    path('login_v/', views.login_v, name='login_v'),
#    path('login/', views.user_login,name='user_login'),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #LoginDemoWithRest

    #upload_profile
    path('upload_profile/', views.upload_profile, name='upload_profile'),
    #open_upload_form
    #simple_upload
    path('open_upload_form/', views.open_upload_form, name='open_upload_form'),
    #path('form_file/', views.form_file, name='form_file'),
    #profile_page
    path('profile_page/', views.profile_page, name='profile_page'),
]


