from datetime import datetime, time

import pytz
from django.test import TestCase

from main.availabilities import get_clinicians_schedule
from main.models import Clinician, ClinicianAvailability


class AvailabilitiesTests(TestCase):

    def _seed_availability(
        self, clinician_id: int, day_of_week: int, start: time, end: time
    ) -> ClinicianAvailability:
        clinician, _ = Clinician.objects.get_or_create(id=clinician_id)
        return ClinicianAvailability.objects.create(
            clinician=clinician,
            day_of_week=day_of_week,
            start=start,
            end=end
        )

    def test_mondays_one_clinician(self):
        # Given Clinician 1 with a schedule on Mondays 9a-12p, 1p-5p
        self._seed_availability(1, ClinicianAvailability.MONDAY, time(hour=9), time(hour=12))
        self._seed_availability(1, ClinicianAvailability.MONDAY, time(hour=13), time(hour=17))

        start_datetime = datetime(2022, 1, 1, tzinfo=pytz.UTC)

        # When forecasting for 14 days (Jan 1st - Jan 14):
        schedules = get_clinicians_schedule(start_datetime, 14)

        # We should get the schedules for 2022-01-03, and 2022-01-10, the two Mondays in that time period
        assert schedules == {
            1: [
                ["2022-01-03T09:00:00+00:00", "2022-01-03T12:00:00+00:00"],
                ["2022-01-03T13:00:00+00:00", "2022-01-03T17:00:00+00:00"],
                ["2022-01-10T09:00:00+00:00", "2022-01-10T12:00:00+00:00"],
                ["2022-01-10T13:00:00+00:00", "2022-01-10T17:00:00+00:00"],
            ]
        }

    def test_thursdays_two_clinicians(self):
        # Given Clinician 1 with a schedule on Thursdays 9a-3p and 12p-5p
        self._seed_availability(1, ClinicianAvailability.WEDNESDAY, time(hour=9), time(hour=15))
        self._seed_availability(3, ClinicianAvailability.WEDNESDAY, time(hour=12), time(hour=17))

        start_datetime = datetime(2022, 1, 1, tzinfo=pytz.UTC)

        # When forecasting for 14 days (Jan 1st - Jan 14):
        schedules = get_clinicians_schedule(start_datetime, 14)

        # We should get the schedules for 2022-01-03, and 2022-01-10, the two Thursday in that time period
        assert schedules == {
            1: [
                ["2022-01-05T09:00:00+00:00", "2022-01-05T15:00:00+00:00"],
                ["2022-01-12T09:00:00+00:00", "2022-01-12T15:00:00+00:00"],
            ],
            3: [
                ["2022-01-05T12:00:00+00:00", "2022-01-05T17:00:00+00:00"],
                ["2022-01-12T12:00:00+00:00", "2022-01-12T17:00:00+00:00"],
            ]
        }

    def test_empty_set(self):
        # Given Clinician 1 with a schedule on Thursdays 9a-3p and 12p-5p
        self._seed_availability(1, ClinicianAvailability.WEDNESDAY, time(hour=9), time(hour=15))
        self._seed_availability(3, ClinicianAvailability.WEDNESDAY, time(hour=12), time(hour=17))

        start_datetime = datetime(2022, 1, 1, tzinfo=pytz.UTC)

        # When forecasting for 3 days (Jan 1st - Jan 3rd; Sun - Tue) that do not include a Wednesday
        schedules = get_clinicians_schedule(start_datetime, 2)

        # We should not get anything
        assert schedules == {}
