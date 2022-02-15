from operator import index
from django.db import models
from django.utils import timezone

# Create your models here.
class Receipts(models.Model):
    receipt_date = models.DateTimeField(default=timezone.now)
    receipt_total = models.DecimalField(max_digits=7, decimal_places=2)
    TIP_SELECTOR = (
        ('default', 'Select Tip'),
        ('15', '15%'),
        ('18', '18%'),
        ('20', '20%'),
        ('22', '22%'),
        ('25', '25%')
    )
    tip_selector = models.CharField(
        max_length=20,
        choices=TIP_SELECTOR,
        default="Select Tip"
    )

    

    class Meta:
        ordering = ['receipt_date']
