import logging
from datetime import datetime
from dateutil.parser import parse
from random import randint
from time import sleep

import pytz
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from main.availabilities import get_clinicians_schedule

PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

ERROR_PERCENTAGE = 15
MAX_DELAY_SECONDS = 7


logger = logging.getLogger(__name__)


class ClinicianAvailabilityView(APIView):

    @staticmethod
    def _get_int_request_param(request: HttpRequest, param_name: str, default_value: int) -> int:
        try:
            value = int(request.GET.get(param_name, default_value))
        except:
            value = default_value
        return value

    @staticmethod
    def _get_datetime_request_param(request: HttpRequest, param_name: str) -> datetime:
        try:
            param = request.GET.get(param_name)
            if param is not None:
                value = parse(param)
            else:
                value = datetime.now(pytz.UTC)
        except:
            raise ValueError("invalid ISO datetime value")
        return value

    @staticmethod
    def _randomly_sleep(seconds: int) -> None:
        sleep_time = randint(0, seconds)
        logger.info(f"Sleeping for {sleep_time} seconds")
        sleep(sleep_time)

    def _randomly_fail(self) -> None:
        if randint(0, 100) < ERROR_PERCENTAGE:
            raise Exception("Bad luck")

    def get(self, request: HttpRequest) -> Response:
        page_size = min(self._get_int_request_param(request, "days_ahead", PAGE_SIZE), MAX_PAGE_SIZE)
        start_datetime = self._get_datetime_request_param(request, "datetime")

        self._randomly_sleep(MAX_DELAY_SECONDS)
        self._randomly_fail()

        output = get_clinicians_schedule(start_datetime, page_size)

        return Response(output)
