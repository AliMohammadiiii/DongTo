from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class debt (models.Model):
    debtor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True, related_name='debtor')
    creditor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True, related_name='creditor')
    price = models.IntegerField()
    is_checkouted = models.BooleanField(default=False)
    date = models.DateTimeField('date published')