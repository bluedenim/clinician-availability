from datetime import time

from django.core.management import BaseCommand

from main.models import Clinician, ClinicianAvailability


class Command(BaseCommand):
    """
    NOTE: the data here is only used for the initial seeding. The actual data in the DB CAN evolve beyond this.
    """
    help = "seed some known clinicians' schedules"

    def handle(self, *args, **options):
        # Create clinicians
        for c in range(1, 5):
            Clinician.objects.get_or_create(id=c)

        schedules = {
            # Clinician 1: Wed, Thu 9a - 5p
            1: [
                (ClinicianAvailability.WEDNESDAY, time(9), time(17)),
                (ClinicianAvailability.THURSDAY, time(9), time(17)),
            ],
            # Clinician 2: Mon, Tue 9a - 12p, 1p - 4:30p
            2: [
                (ClinicianAvailability.MONDAY, time(9), time(12)),
                (ClinicianAvailability.MONDAY, time(13), time(16, 30)),
                (ClinicianAvailability.TUESDAY, time(9), time(12)),
                (ClinicianAvailability.TUESDAY, time(13), time(16, 30)),
            ],
            # Clinician 3: Fri 9a - 12p, 1p - 3p
            3: [
                (ClinicianAvailability.FRIDAY, time(9), time(12)),
                (ClinicianAvailability.FRIDAY, time(13), time(15)),
            ],
            # Clinician 4: Sat 10a - 3p
            4: [
                (ClinicianAvailability.SATURDAY, time(10), time(15)),
            ],
            # Clinician 5: Sun 10a - 3p
            5: [
                (ClinicianAvailability.SUNDAY, time(10), time(15)),
            ],
        }

        for clinician_id, availabilities in schedules.items():
            for day_of_week, start, end in availabilities:
                ClinicianAvailability.objects.get_or_create(
                    clinician_id=clinician_id, day_of_week=day_of_week, start=start, end=end
                )
