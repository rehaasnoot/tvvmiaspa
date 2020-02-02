from django.urls import path
from django.conf.urls import url, include
from .views import PingView, OrderView, ProcessView

urlpatterns = [
    path(PingView.url, view=PingView.as_view(), name=PingView.name),
    path(ProcessView.url, view=ProcessView.as_view(), name=ProcessView.name),
    path(OrderView.url, view=OrderView.as_view(), name=OrderView.name),
#    url(r'^api-auth/', include('rest_framework.urls'))
    path('api-auth/', include('rest_framework.urls'))
]
