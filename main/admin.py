from django import forms
from django.contrib import admin

from main.models import Clinician, ClinicianAvailability


class ClinicianAvailabilityAdmin(admin.ModelAdmin):
    list_display = ("clinician_id", "day_of_week", "start", "end")
    search_fields = ("=clinician_id",)

    def get_search_results(self, request, queryset, search_term):
        queryset = ClinicianAvailability.objects.all()
        try:
            search_term_as_int = int(search_term)
        except ValueError:
            pass
        else:
            queryset = queryset.filter(clinician_id=search_term_as_int)
        return queryset, False


admin.site.register(Clinician)
admin.site.register(ClinicianAvailability, ClinicianAvailabilityAdmin)
