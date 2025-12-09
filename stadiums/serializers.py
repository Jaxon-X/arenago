
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Stadium, StadiumImage


class StadiumImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StadiumImage
        fields = ('image')


class StadiumSerializer(GeoFeatureModelSerializer):
    images = StadiumImageSerializer(many=True)
    class Meta:
        model = Stadium
        geo_field = "location"
        fields = ('owner', 'name', 'address', 'price_per_hour','location', 'is_active', 'created_at', 'images')

        read_only_fields = ('owner', 'created_at')

    def validate_images(self,data):
        if len(data) != 3:
            raise serializers.ValidationError("Images must be equal to 3")

    def create(self, validated_data):

        images_data = validated_data.pop('images')
        stadium = Stadium.objects.create(**validated_data)

        for image_data in images_data:
            image = image_data['image']
            StadiumImage.objects.create(
                stadium=stadium,
                image=image
            )

        return stadium





class StadiumListSerializer(GeoFeatureModelSerializer):
    distance = serializers.SerializerMethodField()
    images = StadiumImageSerializer(many=True)


    class Meta:
        model = Stadium
        geo_field = "location"
        fields = ('distance', 'owner', 'name', 'address', 'price_per_hour','location', 'is_active', 'created_at', 'images')

        read_only_fields = ('owner', 'created_at')

    def get_distance(self, obj):
        return obj.distance.km if obj.distance else None


