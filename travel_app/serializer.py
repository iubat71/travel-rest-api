from rest_framework import serializers
from .models import *

class ContinentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Continent
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'



class AirportSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source="city.name")
    images = serializers.SerializerMethodField()

    class Meta:
        model = Airport
        fields = '__all__'

    def get_images(self, obj):
        request = self.context.get('request')
        return [request.build_absolute_uri(image.image.url) for image in obj.images.all()]


class HotelSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = '__all__'

    def get_images(self, obj):
        request = self.context.get('request')
        return [request.build_absolute_uri(image.image.url) for image in obj.images.all()]


class TripSerializer(serializers.ModelSerializer):
    destination_hotel = HotelSerializer()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = '__all__'

    def get_images(self, obj):
        request = self.context.get('request')
        return [request.build_absolute_uri(image.image.url) for image in obj.images.all()]


class LocationSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = '__all__'

    def get_images(self, obj):
        request = self.context.get('request')
        return [request.build_absolute_uri(image.image.url) for image in obj.images.all()]
