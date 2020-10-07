import ipaddress
from .models.attempt_fail import AttemptFail
from axes.helpers import get_client_ip_address
from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2, GeoIP2Exception
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
import logging


class CountryRestrictionMiddleware(MiddlewareMixin):
    """
    Restrict access to users that are not in an allowed country.

    If GEOIP_COUNTRY_WHITELIST is empty, access blocking is disabled.
    """

    def __init__(self, *args, **kwargs):
        if MiddlewareMixin != object:
            super(CountryRestrictionMiddleware, self).__init__(*args, **kwargs)

        whitelist = settings.GEOIP_COUNTRY_WHITELIST or []
        whitelist = [country.strip().upper() for country in whitelist]
        self.whitelist = whitelist
        self.geoip = GeoIP2()

    def process_request(self, request):
        ip_address = get_client_ip_address(request)
        assert ip_address, ip_address

        request.country_code = None  # Default

        # ip_address = "200.200.100.100" # to uncomment for resuming normal API running

        if ipaddress.ip_address(ip_address).is_private:
            return  # Dev mode, or misconfiguration of portal

        try:
            country = self.geoip.country(ip_address)
            country_code = country["country_code"]  # Should be uppercase
        except GeoIP2Exception:
            country_code = None

        if self.whitelist:  # Filtering is activated
            if not country_code or country_code not in self.whitelist:
                # trace the attempt fail
                AttemptFail.objects.create(
                    ip_client = ip_address,
                    host_client = request.META.get('HTTP_USER_AGENT'),
                    country=country_code)
                logging.error(f"Forbidden acces for  {country_code} country")
                return HttpResponseForbidden("Forbidden country '%s'" % country_code)

        request.country_code = country_code

        return None
