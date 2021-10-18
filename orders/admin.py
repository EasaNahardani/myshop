import csv
import datetime
from django.http import HttpResponse
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Order, OrderItem
from django.utils.translation import ngettext
from django.contrib import messages


# django 3.1 or lower , here write action difinition
# export_to_csv.short_description = 'Export to CSV'

# order_pdf.short_description = 'Invoice'

# making action globally available
# admin.site.add_action(export_to_csv)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated', 'order_detail', 'order_pdf']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = ['export_to_csv']

    @admin.action(description='Export to CSV')
    def export_to_csv(self, request, queryset):
        # opts = self.model._meta
        opts = self.opts
        content_disposition = f'attachment; filename={opts.verbose_name}.csv'
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = content_disposition
        writer = csv.writer(response)
        fields = [field for field in opts.get_fields() if not field.is_relation]
        # Write a first row with header information
        writer.writerow([field.verbose_name for field in fields])
        # Write data rows
        for obj in queryset:
            data_row = []
            for field in fields:
                value = getattr(obj, field.name)
                if isinstance(value, datetime.datetime):
                    value = value.strftime('%d/%m/%Y')
                data_row.append(value)
            writer.writerow(data_row)
        # to flash a message to the user informing them that the action was successful
        self.message_user(request, ngettext(
            '%s object was successfully downloaded as CSV.',
            '%s objects was successfully downloaded as CSV.',
            queryset.count(),
        ) % opts.verbose_name, messages.SUCCESS)
        return response

    @admin.display(description='Order Details')
    def order_detail(self, obj):
        url = reverse('orders:admin_order_detail', args=[obj.id])
        return mark_safe(f'<a href="{url}">View</a>')

    @admin.display(description='Invoice')
    def order_pdf(self, obj):
        url = reverse('orders:admin_order_pdf', args=[obj.id])
        return mark_safe(f'<a href="{url}">PDF</a>')
