from django.db import models

# Create your models here.
class City(models.Model):
    # this model table only stores city names
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'cities'
