from django.contrib import admin
from .models import (
    Amenity,
    Bus,
    Route,
    Seat,
    Trip,
    Driver,
    Passenger,
    Town,
    Booking
)

# Register your models here.
admin.site.register(Amenity)
admin.site.register(Bus)
admin.site.register(Route)
admin.site.register(Seat)
admin.site.register(Trip)
admin.site.register(Driver)
admin.site.register(Passenger)
admin.site.register(Town)
admin.site.register(Booking)