from datetime import date, datetime
from typing import Tuple

import pytz
from django.db import models


class Clinician(models.Model):
    def __str__(self) -> str:
        return f"Clinician(id={self.id})"


class ClinicianAvailability(models.Model):
    # These constants match the datetime.weekday() semantics
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6
    DAYS_OF_WEEK = [
        (MONDAY, "Monday"),
        (TUESDAY, "Tuesday"),
        (WEDNESDAY, "Wednesday"),
        (THURSDAY, "Thursday"),
        (FRIDAY, "Friday"),
        (SATURDAY, "Saturday"),
        (SUNDAY, "Sunday"),
    ]

    clinician = models.ForeignKey("Clinician", on_delete=models.CASCADE)
    day_of_week = models.PositiveIntegerField(
        "Day of Week",
        choices=DAYS_OF_WEEK,
        null=False,
        blank=False
    )
    start = models.TimeField(null=False, blank=False)
    end = models.TimeField(null=False, blank=False)

    def datetime_on_date(self, the_date: date) -> Tuple[datetime, datetime]:
        """
        create a tuple of datetimes by attaching the instance's start and end times to the date provided.

        :param the_date: the date to attach the start and end times to

        :return: a 2-tuple of datetimes indicating the start and end datetimes
        """
        return (
            datetime.combine(the_date, self.start, tzinfo=pytz.UTC),
            datetime.combine(the_date, self.end, tzinfo=pytz.UTC)
        )
