from django.contrib.gis.db import models
from django.contrib.gis.geos import Point


class Peak(models.Model):
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    altitude = models.FloatField(null=False)
    name = models.CharField(max_length=100)
    location = models.PointField(help_text='the location of the peak')


    def __str__(self):
        return f"{self.latitude} {self.longitude} {self.altitude} {self.name}"


    def save(self, *args, **kwargs):
        self.location = Point(x=self.longitude, y=self.latitude)
        return super().save(*args, **kwargs)

