from collections import defaultdict
from datetime import date, timedelta
import logging
from typing import Dict, List

from main.models import ClinicianAvailability

logger = logging.getLogger(__name__)


def get_clinicians_schedule(start_date: date, days_horizon: int) -> Dict[int, List[List[str]]]:
    """
    Given a start datetime and number of days ahead to look, build a dict of start/end datetimes for all availabilities
    for all clinicians. The values for the datetimes will be in the ISO 8601 format. An example output::

        {
            1: [
                ["2022-01-01T09:00:00+00:00", "2022-01-01T17:00:00+00:00"],
                ["2022-01-07T09:00:00+00:00", "2022-01-07T17:00:00+00:00"]
            ],
            2: [
                ["2022-01-03T10:00:00+00:00", "2022-01-03T12:00:00+00:00"]
            ]
        }


    :param start_date: the start date/time to find availabilities
    :param days_horizon: the number of days to the future to include

    :returns: a dict of start/end date/times for availabilities, keyed by the clinician ID
    """
    start_weekday = start_date.weekday()

    schedules = defaultdict(list)  # type: Dict[int, List[List[str]]]
    day_of_weeks = [
        (start_weekday + d) % 7
        for d in range(min(7, days_horizon + 1))
    ]

    # Build a map of days-of-week to ClinicianAvailabilities that fall on the day of week (e.g. Mondays)
    availabilities_by_day_of_week = defaultdict(list)  # type: Dict[int, List[ClinicianAvailability]]
    for ca in ClinicianAvailability.objects.filter(day_of_week__in=day_of_weeks):
        availabilities_by_day_of_week[ca.day_of_week].append(ca)

    # Iterate over the days starting from start_date
    for datetime_offset in range(days_horizon + 1):
        the_datetime = start_date + timedelta(days=datetime_offset)
        day_of_week = the_datetime.weekday()

        # Convert all the ClinicianAvailability records on this day-of-week to start/end entries and append to the
        # clinician ID's list of start/end entries
        for ca in availabilities_by_day_of_week[day_of_week]:
            schedules[ca.clinician_id].append(
                [dt.isoformat() for dt in ca.datetime_on_date(the_datetime)]
            )

    return dict(schedules)
