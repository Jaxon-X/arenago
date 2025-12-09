


from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):


    class Meta:
        model = Booking
        fields = ('user', 'stadium', 'start_time', 'end_time', 'created_at', 'total_price', 'payment_status')
        read_only_fields = ['total_price']

    def validate(self, data):

        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError('Start time must be before end time')

    def validate_total_price(self, value):
       if value:
           raise serializers.ValidationError("Total price is calculated automatically and cannot be set manually.")

    def create(self, validated_data):
        stadium_instance = validated_data['stadium']
        calculated_total_price = stadium_instance.price_per_hour / 2
        validated_data['total_price'] = calculated_total_price

        booking = Booking.objects.create(**validated_data)

        return booking

