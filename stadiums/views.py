from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

from .models import Stadium
from .serializers import StadiumSerializer
from .permissions import IsObjectOwner


class StadiumListCreateView(generics.ListCreateAPIView):
    queryset = Stadium.objects.all()
    serializer_class = StadiumSerializer
    permission_classes = [IsAuthenticated, IsObjectOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class StadiumDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stadium.objects.all()
    serializer_class = StadiumSerializer
    permission_classes = [IsAuthenticated, IsObjectOwner]


class StadiumNearByView(generics.ListAPIView):
    serializer_class = StadiumSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        lat = self.request.query_params.get('lat')
        lon = self.request.query_params.get('lon')

        if lat and lon:
            try:
                latitude = float(lat)
                longitude = float(lon)

                user_location = Point(latitude, longitude, srid=4326)

                return Stadium.objects.annotate(
                    distance = Distance('location', user_location)).order_by('distance')
            except ValueError:
                return Stadium.objects.all()

        return Stadium.objects.all()

