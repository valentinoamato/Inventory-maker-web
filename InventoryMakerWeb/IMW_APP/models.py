from django.db import models
from django.conf import settings

# Create your models here.
class inventory(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    description = models.CharField(max_length=1000,null=True)

    def __str__(self):
        return f"{self.name}-{self.user}"
        
    def GetName(ivt):
        return ivt.name
    
    def GetId(ivt):
        return ivt.id

class items(models.Model):
    ivt = models.ForeignKey(inventory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000,null=True)
    quantity = models.IntegerField(null=True)
    unity = models.CharField(max_length=50,null=True)
    
    def GetName(itm):
        return itm.name
    
    def GetId(itm):
        return itm.id




