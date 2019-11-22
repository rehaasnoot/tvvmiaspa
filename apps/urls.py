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
from .settings import MEDIA_ROOT, MEDIA_URL, STATIC_URL, STATIC_ROOT
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
from graphene_django.views import GraphQLView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from apps.tvvroot import views as rootv
from apps.user_registration import views as regv

urlpatterns = [
    path('admin/', admin.site.urls, name='Admin', kwargs=None),
    path('graphql/', GraphQLView.as_view(graphiql=True), name='GraphQL', kwargs=None),
    path('current_datetime/', view=rootv.current_datetime, name='Now', kwargs=None),
#    path('register_user/', view=regv.RegisterView.as_view(), name='Register User', kwargs=None),
    url(r'^register/', view=regv.RegisterView.as_view(template_name="register.html"), name="Register User"),
    path('', view=rootv.IndexView.as_view(), name='index', kwargs=None),
    path('app', view=rootv.AppView.as_view(), name='App', kwargs=None),
    path('create', view=rootv.CreateView.as_view(), name='Create', kwargs=None),
    path('about', view=rootv.AboutView.as_view(), name='About', kwargs=None),
    path('login', view=rootv.TVVLoginView.as_view(), name='Login', kwargs=None),
    path('videos/', view=rootv.VideosView.as_view(), name='Videos'),
    path('video/<int:video_id>/', view=rootv.VideoView.as_view(), name="video"),
    path('orders', view=rootv.OrderView.as_view(), name='Orders', kwargs=None),
]
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

