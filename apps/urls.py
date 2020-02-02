"""apps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from apps.settings import MEDIA_ROOT, MEDIA_URL, STATIC_URL, STATIC_ROOT
from django.contrib import admin, staticfiles
from django.urls import path, re_path
from django.conf.urls import url, include
from django.conf.urls.static import static
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from graphene_django.views import GraphQLView
#from django.contrib.auth.views import LoginView, LogoutView
#from django.contrib.auth import views as auth_views
#from django.contrib.auth.decorators import login_required
from apps.tvvroot import views as rootv
from apps.tvvroot import forms as rootf
from apps.user_registration import views as regv
from apps.api_v1.urls import urlpatterns as apiurls

urlpatterns = [
    path('', view=rootv.IndexView.as_view(), name=rootv.IndexView.name),
    path('admin/', admin.site.urls, name='Admin'),
    path('graphql/', GraphQLView.as_view(graphiql=True), name='GraphQL'),
    path('current_datetime/', view=rootv.current_datetime, name='now'),
    url('^registration/', include("apps.user_registration.urls") ),
    path('app/', view=rootv.AppView.as_view(), name=rootv.AppView.name),
    url(r'^about/$', view=rootv.AboutView.as_view(), name=rootv.AboutView.name),
    path('login/', view=rootv.TVVLoginView.as_view(), name=rootv.TVVLoginView.name),
    path('logout/', view=rootv.TVVLogoutView.as_view()),
    path('videos/', view=rootv.VideosView.as_view(), name=rootv.VideosView.name),
    path('video/<int:video_id>/', view=rootv.VideoView.as_view(), name=rootv.VideosView.name),
    url(r'^orders/', view=rootv.OrdersView.as_view(), name=rootv.OrdersView.name),
    url(r'^order/purchase/(?P<pk>\d+)$', view=rootv.OrderPurchaseView.as_view(), name=rootv.OrderPurchaseView.name),
    url(r'^order/create/', view=rootv.OrderCreateView.as_view(), name=rootv.OrderCreateView.name),
#    url(r'^order/update/', view=rootv.OrderUpdate.as_view(), name=rootv.OrderUpdate.name),
#    url(r'^order/delete/', view=rootv.OrderDelete.as_view(), name=rootv.OrderDelete.name),
#    url(r'^order/submit/(?P<pk>\d+)$', view=rootv.OrderSubmit.as_view(), name=rootv.OrderSubmit.name),
    re_path(r'^order/detail/(?P<pk>\d+)$', view=rootv.OrderDetailView.as_view(), name=rootv.OrderDetailView.name),
#    path('order/detail/<int:pk>/', view=rootv.OrderDetailView.as_view(), name=rootv.OrderDetailView.name),
    path('blagent/', view=rootv.TVVBlagentView.as_view(), name=rootv.TVVBlagentView.name),
    re_path(r'^fib/(?P<n>\d+)$', view=rootv.WWWfibonacci, name='fibonacci'),
]

urlpatterns += apiurls

urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)


from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import SimpleTestCase, override_settings

def response_error_handler(request, exception=None):
    return HttpResponse('Error handler content', status=403)

def permission_denied_view(request):
    raise PermissionDenied

urlpatterns += [
    path('403/', permission_denied_view),
]

handler403 = response_error_handler

# ROOT_URLCONF must specify the module that contains handler403 = ...
@override_settings(ROOT_URLCONF=__name__)
class CustomErrorHandlerTests(SimpleTestCase):

    def test_handler_renders_template_response(self):
        response = self.client.get('/403/')
        # Make assertions on the response here. For example:
        self.assertContains(response, 'Error handler content', status_code=403)

