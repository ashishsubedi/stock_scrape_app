from django.contrib import admin
from .models import Stock, StockRecord

class StockRecordInline(admin.TabularInline):
    model = StockRecord
    extra = 2
    show_change_link = True

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return True



class StockAdmin(admin.ModelAdmin):
    inlines = [StockRecordInline]
    readonly_fields = ['name']

admin.site.register(Stock, StockAdmin)