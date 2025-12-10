from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

from .models import Stadium
from .serializers import StadiumSerializer, StadiumListSerializer
from .permissions import IsObjectOwner


class StadiumListCreateView(generics.ListCreateAPIView):
    serializer_class = StadiumSerializer
    permission_classes = [IsAuthenticated, IsObjectOwner]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Stadium.objects.none()

        return Stadium.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class StadiumDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stadium.objects.all()
    serializer_class = StadiumSerializer
    permission_classes = [AllowAny, IsObjectOwner]


class StadiumNearByView(generics.ListAPIView):
    serializer_class = StadiumListSerializer
    permission_classes = [AllowAny] #keyin isAuthenticatedga o'zgartirish kerak

    def get_queryset(self):
        lat = self.request.query_params.get('lat')
        lon = self.request.query_params.get('lon')

        if lat and lon:
            try:
                latitude = float(lat)
                longitude = float(lon)

                user_location = Point(longitude, latitude, srid=4326)

                return Stadium.objects.annotate(
                    distance = Distance('location', user_location)).order_by('distance')
            except ValueError:
                return Stadium.objects.none()

        return Stadium.objects.all()


class StadiumViewByFilter(generics.ListAPIView):
    serializer_class = StadiumListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Stadium.objects.all()
        order_by_field = 'name'

        lat = self.request.query_params.get('lat')
        lon = self.request.query_params.get('lon')

        if lat and lon:
            try:
                latitude = float(lat)
                longitude = float(lon)
                user_location = Point(longitude, latitude, srid=4326)

                queryset = queryset.annotate(
                    distance=Distance('location', user_location)
                )
                order_by_field = 'distance'

            except (ValueError, TypeError):
                raise ValidationError("Kordinatalar formati noto'g'ri. Iltimos, raqam kiriting.")

        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if min_price is not None and max_price is not None:
            try:
                min_price_float = float(min_price)
                max_price_float = float(max_price)

                queryset = queryset.filter(
                    price_per_hour__range=(min_price_float, max_price_float)
                )
            except (ValueError, TypeError):
                raise ValidationError("Narx qiymatlari formati noto'g'ri. Iltimos, faqat raqam kiriting.")

        return queryset.order_by(order_by_field)



