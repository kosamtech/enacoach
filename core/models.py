from django.db import models


class CommonInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Amenity(CommonInfo):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Seat(CommonInfo):
    class SeatChoice(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        RESERVED = 'reserved', 'Reserved'
        BOOKED = 'booked', 'Booked'
    status = models.CharField(
        max_length=10,
        choices=SeatChoice.choices,
        default=SeatChoice.AVAILABLE
    )
    seat_number = models.CharField(max_length=10)

    def __str__(self):
        return self.seat_number


class Bus(CommonInfo):
    name = models.CharField(max_length=50)
    seats = models.ManyToManyField(Seat, blank=True)
    amenities = models.ManyToManyField(Amenity)
    bus_type = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Route(CommonInfo):
    origin = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    distance = models.IntegerField()
    duration = models.IntegerField()
    buses = models.ManyToManyField(Bus)

    def __str__(self):
        return f'{self.origin} to {self.destination}'


class Trip(CommonInfo):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    departure_date = models.DateField()
    arrival_date = models.DateField()
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    price = models.FloatField()
    seats = models.ManyToManyField(Seat)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.bus.name} - {self.route.origin} to {self.route.destination}'

    @property
    def available_seats(self):
        return self.seats.filter(status=Seat.SeatChoice.AVAILABLE).count()

    @property
    def booked_seats(self):
        return self.seats.filter(status=Seat.SeatChoice.BOOKED).count()

    @property
    def reserved_seats(self):
        return self.seats.filter(status=Seat.SeatChoice.RESERVED).count()


class Passenger(CommonInfo):
    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    national_id = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    age = models.IntegerField()
    nationality = models.CharField(max_length=20)
    countrycode = models.CharField(max_length=4)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Booking(CommonInfo):
    class BookingStatus(models.TextChoices):
        PENDING_PAYMENT = "pending payment", "Pending Payment"
        PAID = "paid", "Paid"
        PRINTED = "printed", "Printed"
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=BookingStatus.choices, default=BookingStatus.PENDING_PAYMENT)
    reference = models.CharField(max_length=50)
    is_paid = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    is_refunded = models.BooleanField(default=False)
    date_of_travel = models.DateField(blank=True, null=True)


    def __str__(self):
        return f'{self.trip.bus.name} - {self.trip.route.origin} to {self.trip.route.destination}'


class Payment(CommonInfo):
    class PaymentChoice(models.TextChoices):
        MPESA = 'mpesa', 'Mpesa'
        CARD = 'card', 'Card'
        CASH = 'cash', 'Cash'

    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SUCCESS = 'success', 'Success'
        FAILED = 'failed', 'Failed'

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.FloatField()
    method = models.CharField(max_length=10, choices=PaymentChoice.choices, default=PaymentChoice.MPESA)
    status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)

    def __str__(self):
        return f'{self.booking.reference} - {self.amount}'


class Town(CommonInfo):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Driver(CommonInfo):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    id_number = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'