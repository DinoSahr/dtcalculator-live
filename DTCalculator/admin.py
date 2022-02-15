from shutil import ReadError
from django.contrib import admin
from .models import Receipts

# Register your models here.
class ReceiptsAdmin(admin.ModelAdmin):
    list_display = ('id', 'receipt_date', 'receipt_total', 'tip_selector')




admin.site.register(Receipts, ReceiptsAdmin)