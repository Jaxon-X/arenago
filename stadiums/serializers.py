

from rest_framework_gis.serializers import GeoFeatureModelSerializer
from models import Stadium

class StadiumSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Stadium
        geo_field = "location"
        fields = ('owner', 'name', 'address', 'price_per_hour','location', 'is_active', 'created_at')

        read_only_fields = ('owner', 'created_at')



