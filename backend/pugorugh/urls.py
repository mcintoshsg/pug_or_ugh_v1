from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from pugorugh.views import (UserRegisterView, 
                    ListCreateDogView, 
                    RetrieveUpdateDestroyDogView,
                    RetrieveUpdateUserPrefView,
                    RetrieveUpdateLDUDogView,
                    )

app_name = 'pugorugh'

# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^api/user/login/$', obtain_auth_token, name='login-user'),
    url(r'^api/user/$', UserRegisterView.as_view(), name='register-user'),

    # url for the logged in users doggie prferences 
    url(r'^api/user/preferences/$',
        RetrieveUpdateUserPrefView.as_view(),
        name='userprefs'),

    # list out all doggies created 
    url(r'^api/alldogs/', ListCreateDogView.as_view(), name='dog-listcreate'),
    url(r'^api/alldogs/(?P<pk>\d+)$',
            RetrieveUpdateDestroyDogView.as_view(),
            name='dog-rud'),

   # urls for likes, dislikes, undecided
    url(r'^api/dog/(?P<pk>-?\d+)/(?P<ldu_decision>\w+)/(next/)?$',
            RetrieveUpdateLDUDogView.as_view(),
            name='dog-ldu'),
   
    url(r'^favicon\.ico$',
        RedirectView.as_view(
            url='/static/icons/favicon.ico',
            permanent=True
        )),
    url(r'^$', TemplateView.as_view(template_name='index.html')),

])
