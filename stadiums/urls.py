

from django.urls import path

from stadiums.views import StadiumListCreateView, StadiumDetailView, StadiumNearByView, StadiumViewByFilter

urlpatterns = [
    path('', StadiumListCreateView.as_view(), name='stadium-list'),
    path('<int:pk>/', StadiumDetailView.as_view(), name='stadium-detail'),
    path('nearest/', StadiumNearByView.as_view(), name='stadium-nearest'),
    path('stadiums/', StadiumViewByFilter.as_view(), name='stadium-filter')

]