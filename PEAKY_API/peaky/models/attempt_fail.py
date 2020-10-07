from django.db import models

# Model to trace failed attempts
class AttemptFail(models.Model):
    ip_client = models.CharField(max_length=30)
    host_client = models.CharField(max_length=500)
    country = models.CharField(max_length=2)
    date_attempt = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.ip_client} {self.country}"

