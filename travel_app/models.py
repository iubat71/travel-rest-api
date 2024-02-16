from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from account.models import User

class Continent(models.Model):
    class Name(models.TextChoices):
        EUROPE = "Europe"
        NORTH_AMERICA = "North America"
        SOUTH_AMERICA = "South America"
        ASIA = "Asia"
        AUSTRALIA_OCEANIA = "Australia & Oceania"
        AFRICA = "Africa"

    name = models.CharField(choices=Name.choices, max_length=32, unique=True)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=50)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE, related_name="countries")

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=150)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities")

    def __str__(self):
        return self.name

class AirportImage(models.Model):
    image = models.ImageField(upload_to='airport_images/')

class Airport(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="airports")
    images = models.ManyToManyField(AirportImage, related_name="airport_image")


    def __str__(self):
        return self.name
    

class HotelImage(models.Model):
    image = models.ImageField(upload_to='hotel_images/')

class Hotel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hotels")
    name = models.CharField(max_length=50)
    standard = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    description = models.TextField(blank=True, null=True, max_length=250)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="hotels")
    images = models.ManyToManyField(HotelImage, related_name="hotel_image")
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    def __str__(self):
        return self.name

class Type(models.TextChoices):
    BED_AND_BREAKFAST = "BB"
    HALF_BOARD = "HB"
    FULL_BOARD = "FB"
    ALL_INCLUSIVE = "AI"

class TripImage(models.Model):
    image = models.ImageField(upload_to='trip_images/')


class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trips")
    type = models.CharField(choices=Type.choices, max_length=2)
    days_number = models.PositiveSmallIntegerField()
    departure_date = models.DateTimeField()
    return_date = models.DateTimeField()
    price_adults = models.FloatField()
    price_kids = models.FloatField()
    is_promoted = models.BooleanField(default=False)
    places_for_adults = models.PositiveSmallIntegerField()
    places_for_kids = models.PositiveSmallIntegerField()
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, null=True, related_name="trips_departure")
    destination_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, null=True, related_name="trips_destination")
    destination_hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, related_name="trips_hotel")
    images = models.ManyToManyField(TripImage,related_name="trip_image")
    def __str__(self):
        return f"Trip to {self.destination_hotel.name}"



class LocationImage(models.Model):
    image = models.ImageField(upload_to='trip_images/')


class Location(models.Model):
    street = models.CharField(max_length=200)
    number = models.CharField(max_length=20)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="locations_city")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="locations_country")
    images = models.ManyToManyField(LocationImage ,related_name="location_image")

    def __str__(self):
        return f"{self.street} {self.number} {self.city} {self.country}"

class Holiday(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    duration = models.IntegerField()
    price = models.FloatField()
    free_slots = models.IntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_booking_trips")
    trip=models.ForeignKey(Trip,on_delete=models.CASCADE,related_name="booking_trip")
    holiday = models.ForeignKey(Holiday, on_delete=models.CASCADE)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="booking")
    hotel=models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, related_name="booking_hotel")



