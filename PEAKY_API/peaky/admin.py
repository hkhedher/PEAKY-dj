from django.contrib import admin
from .models.attempt_fail import AttemptFail
from .models.peak import Peak


@admin.register(AttemptFail)
class AttemptFailAdmin(admin.ModelAdmin):
    list_display = ("ip_client", "host_client", "country", "date_attempt")

@admin.register(Peak)
class PeakAdmin(admin.ModelAdmin):
    list_display = ("name","location")
