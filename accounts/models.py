from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class OrderModel(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    customer_name = models.CharField(max_length=200)
    service_charge = models.FloatField(max_length=50)
    parts_cost = models.FloatField(max_length=50)
    refreshment_cost = models.FloatField(max_length=50)
    date_created = models.DateTimeField(
        auto_now_add=True)

    def __str__(self):
        return self.customer_name
