from django.db import models
from django.conf import settings

# Create your models here.
class inventory(models.Model):
    title = models.CharField(max_length=1000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"{self.title}-{self.user}"
        

class items(models.Model):
    ivt = models.ForeignKey(inventory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)




