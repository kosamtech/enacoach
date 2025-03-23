import json
import string
import random
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.middleware.csrf import get_token
from django.views import View
from django.http import JsonResponse

from .models import Town, Trip, Passenger, Seat, Booking, Payment
from .forms import SearchForm

# Create your views here.

class IndexView(View):
    def get(self, request):
        towns = Town.objects.all()
        context = {
            'towns': towns,
            'csrf_token': get_token(request)
        }
        return render(request, 'core/index.html', context)

    def post(self, request):
        form = SearchForm(request.POST)
        towns = Town.objects.all()
        context = {"towns": towns}

        if not form.is_valid():
            context.update({"errors": form.errors})
            return render(request, "core/index.html", {"errors": form.errors})

        origin = form.cleaned_data.get("origin")
        destination = form.cleaned_data.get("destination")
        travel_date = form.cleaned_data.get("travel_date")

        if origin == destination:
            context.update({"errors": {"message": "From and To cannot be the same"}})
            return render(request, "core/index.html", context)

        url = reverse("searchresult") + f"?origin={origin}&destination={destination}&travel_date={travel_date}"

        return redirect(url)


class AboutView(View):
    def get(self, request):
        return render(request, 'core/about.html')


class ContactView(View):
    def get(self, request):
        return render(request, 'core/contact.html')


class GalleryView(View):
    def get(self, request):
        return render(request, 'core/gallery.html')


class ManageTicketView(View):
    def get(self, request):
        context = {}

        if request.GET:
            reference = request.GET.get("reference")
            countrycode = request.GET.get("countrycode")
            phone_number = request.GET.get("phone_number")

            bookings = Booking.objects.filter(reference=reference, passenger__phone_number=phone_number, passenger__countrycode=countrycode)
            print(bookings)
            context.update({"bookings": bookings})
        return render(request, 'core/manageticket.html', context)

class ManageTicketDetailView(View):
    def get(self, request, pk):

        booking = get_object_or_404(Booking, pk=pk)
        context = {"booking": booking}

        return render(request, 'core/manage-ticket-detail.html', context)

    def post(self, request, pk):
        date_of_travel = request.POST.get("date_of_travel")
        booking = get_object_or_404(Booking, pk=pk)
        booking.date_of_travel = date_of_travel
        booking.save()
        context = {"booking": booking, "message": "Your ticket has been successfully rescheduled!"}
        return render(request, 'core/manage-ticket-detail.html', context)



class SignInView(View):
    def get(self, request):
        return render(request, 'core/signin.html')


class SearchResultView(View):
    def get(self, request):
        origin = request.GET.get("origin")
        destination = request.GET.get("destination")
        travel_date = request.GET.get("travel_date")

        results = Trip.objects.filter(departure_date=travel_date, route__origin=origin, route__destination=destination)
        a_seats = []
        b_seats = []
        for trip in results:
            for seat in trip.seats.all():
                if 'a' in seat.seat_number.lower():
                    a_seats.append(seat)
                elif 'b' in seat.seat_number.lower():
                    b_seats.append(seat)

        context = {
            "results": results,
            "origin": origin,
            "destination": destination,
            "travel_date": datetime.strptime(travel_date, '%Y-%m-%d').strftime("%B %d, %Y"),
            "a_seats": a_seats,
            "b_seats": b_seats
        }

        return render(request, 'core/searchresult.html', context)

    def post(self, request):
        print(request.POST)
        query_dict = dict(request.POST)
        booking = json.loads(query_dict.pop("booking")[0])
        query_dict.pop("csrfmiddlewaretoken")
        email = query_dict.pop("email")[0]

        passengers = self.get_cleaned_passengers(query_dict, booking["seats"], email)

        trip = get_object_or_404(Trip, pk=booking["trip"]["tripId"])

        seats = []
        seat_prices = []

        for seat in booking["seats"]:
            seat_obj = Seat.objects.get(pk=seat["seatId"])
            seat_obj.status = Seat.SeatChoice.BOOKED
            seat_obj.save()
            seats.append(seat_obj)
            seat_prices.append(int(float(seat["price"])))

        total_payable = sum(seat_prices)
        reference = self.generate_reference()

        for index, passenger in enumerate(passengers):
            pass_obj = Passenger.objects.create(**passenger)

            booking_obj = Booking.objects.create(
                trip=trip,
                passenger=pass_obj,
                seat=seats[index],
                reference=reference,
            )
            Payment.objects.create(booking=booking_obj,amount=seat_prices[index])

        return JsonResponse({
            "message": "booking made successfully",
            "status": "success",
            "total_payable": total_payable,
            "payment_reference": reference,
            "trip": trip.id
        })

    def get_cleaned_passengers(self, query_dict: dict, seats: list, email):
        cleaned_obj = {}
        passengers = []
        for key, value in query_dict.items():
            cleaned_obj[key] = value[0]

        for seat in seats:
            pass_obj = {}
            full_name = cleaned_obj[f"{seat["seatNumber"]}.fullName"].split(" ")
            try:
                pass_obj["first_name"] = full_name[0]
                pass_obj["last_name"] = full_name[1]
            except:
                pass
            pass_obj["gender"] = cleaned_obj[f"{seat["seatNumber"]}.gender"]
            pass_obj["age"] = cleaned_obj[f"{seat["seatNumber"]}.age"]
            pass_obj["countrycode"] = cleaned_obj[f"{seat["seatNumber"]}.countrycode"]
            pass_obj["phone_number"] = cleaned_obj[f"{seat["seatNumber"]}.phone_number"]
            pass_obj["nationality"] = cleaned_obj[f"{seat["seatNumber"]}.nationality"]
            pass_obj["national_id"] = cleaned_obj[f"{seat["seatNumber"]}.national_id"]
            passengers.append(pass_obj)

        passengers[0]["is_primary"] = True
        passengers[0]["email"] = email

        return passengers

    def generate_reference(self, length=10):
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choices(characters, k=length))


class PaymentView(View):
    def get(self, request):
        total_payable = request.GET.get("amount")
        reference = request.GET.get("reference")
        trip = request.GET.get("trip")
        context = {
            "total_payable": total_payable,
            "reference": reference,
            "trip": trip
        }
        return render(request, 'core/payment.html', context)

    def post(self, request):
        print(request.POST)
        trip = request.POST.get("trip")
        reference = request.POST.get("reference")
        amount = request.POST.get("amount")

        trip = get_object_or_404(Trip, pk=trip)
        bookings = Booking.objects.filter(trip=trip, reference=reference)
        payable = sum([b.trip.price for b in bookings])
        if payable != float(amount):
            return JsonResponse({"message": f"Kindly pay {payable}"}, status=400)

        for booking in bookings:
            booking.is_paid = True
            booking.status = Booking.BookingStatus.PAID
            booking.date_of_travel = booking.trip.departure_date
            booking.save()
            booking.payment.status = Payment.PaymentStatus.SUCCESS
            booking.payment.save()

        return JsonResponse({"message": "Confirmed! Your ticket has been successfully booked"})
