import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Bus, Seat

logger = logging.getLogger(__file__)


@receiver(post_save, sender=Bus)
def assign_seats(sender, instance, created, **kwargs):
    logger.info("Bus instance was created", instance.name)
    print("printing..... Bus instance was created", instance.name)
    if created:
        a_seats_count, b_seats_count = 12, 12

        for i in range(a_seats_count):
            seat = Seat.objects.create(seat_number=f"A{i+1}")
            logger.info(f"seat with id A{i+1} created")
            instance.seats.add(seat)

        for i in range(b_seats_count):
            seat = Seat.objects.create(seat_number=f"B{i+1}")
            logger.info(f"seat with id B{i + 1} created")
            instance.seats.add(seat)

        logger.info("Seats created and assigned to bus instance was created")

