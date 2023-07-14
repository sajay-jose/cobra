from django.db import models

# Create your models here.
class bank(models.Model):
  Ac_no = models.IntegerField(unique=True)
  name = models.CharField(max_length=50)
  amount = models.IntegerField()
  phone = models.IntegerField()
  password = models.CharField(max_length=120)
  def __str__(self):
    return self.name
