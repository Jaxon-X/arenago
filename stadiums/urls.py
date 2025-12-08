

from django.urls import path

from stadiums.views import StadiumListCreateView, StadiumDetailView, StadiumNearByView

urlpatterns = [
    path('', StadiumListCreateView.as_view(), name='stadium-list'),
    path('<int:pk>/', StadiumDetailView.as_view(), name='stadium-detail'),
    path('nearest/', StadiumNearByView.as_view(), name='stadium-nearest')

]