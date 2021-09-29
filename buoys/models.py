from django.db import models
from core.models import TimeStampedModel
from users.models import User

# Create your models here.


class Buoy(TimeStampedModel):

    """Buoy Model Definition"""

    # 추후 설치된 부표 buoyname, coordinates, startup, downtime을 가져오고 가동중이면 operation True
    model_number = models.CharField(max_length=140)
    lat = models.FloatField(default=0)
    lon = models.FloatField(default=0)
    temperature = models.FloatField(default=0)
    oxygen = models.FloatField(default=0)
    hydrogen = models.FloatField(default=0)
    salt = models.FloatField(default=0)
    turbidity = models.FloatField(default=0)
    startup = models.DateTimeField()
    downtime = models.DateTimeField()
    operation = models.BooleanField(default=False)
    host = models.ForeignKey(User, related_name="buoys", on_delete=models.CASCADE)
    measurement_time = models.DateTimeField()

    def __str__(self):
        return self.model_number
