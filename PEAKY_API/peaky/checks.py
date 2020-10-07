from django.conf import settings
from django.core.checks import Warning, register, Tags

@register(Tags.security)
def check_country_whitelist(app_configs, **kwargs):

    errors = []
    whitelist = getattr(settings, "GEOIP_COUNTRY_WHITELIST", None)

    success = False
    if isinstance(whitelist, (list, tuple)):
        if all(isinstance(country, str) for country in whitelist):
            success = True

    if not success:
        errors.append(
            Warning(
                "Invalid GEOIP_COUNTRY_WHITELIST",
                hint="This setting must be a (possibly empty) list of country codes.",
                obj=None,
                id="accounts.E100",
            )
        )
    return errors

