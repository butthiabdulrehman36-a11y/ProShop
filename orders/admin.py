from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

    readonly_fields = (
        'product_image',
        'item_total',
    )

    fields = (
        'product_image',
        'product',
        'quantity',
        'price',
        'item_total',
    )

    @admin.display(description='Image')
    def product_image(self, obj):
        if obj.product and obj.product.image:
            return format_html(
                '<img src="{}" width="60" height="60" '
                'style="object-fit:cover; border-radius:8px;" />',
                obj.product.image.url,
            )

        return 'No Image'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'customer_id_link',
        'customer_name_link',
        'email',
        'phone',
        'city',
        'total_amount',
        'item_quantity',
        'status_badge',
        'created_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'name',
        'email',
        'phone',
        'city',
        'address',
        'user__username',
    )

    readonly_fields = (
        'created_at',
        'total_amount',
        'item_quantity',
    )

    ordering = (
        '-created_at',
    )

    list_per_page = 20

    date_hierarchy = 'created_at'

    inlines = [
        OrderItemInline,
    ]

    fieldsets = (
        (
            'Customer Information',
            {
                'fields': (
                    'user',
                    'name',
                    'email',
                    'phone',
                    'address',
                    'city',
                )
            },
        ),
        (
            'Order Information',
            {
                'fields': (
                    'total_amount',
                    'item_quantity',
                    'status',
                    'created_at',
                )
            },
        ),
    )

    @admin.display(
        description='Customer ID',
        ordering='id',
    )
    def customer_id_link(self, obj):
        url = reverse(
            'admin:orders_order_change',
            args=[obj.pk],
        )

        return format_html(
            '<a href="{}"><strong>#{}</strong></a>',
            url,
            obj.pk,
        )

    @admin.display(
        description='Customer Name',
        ordering='name',
    )
    def customer_name_link(self, obj):
        url = reverse(
            'admin:orders_order_change',
            args=[obj.pk],
        )

        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.name,
        )

    @admin.display(
        description='Quantity',
    )
    def item_quantity(self, obj):
        return sum(
            item.quantity
            for item in obj.items.all()
        )

    @admin.display(
        description='Status',
    )
    def status_badge(self, obj):
        return format_html(
            '<strong>{}</strong>',
            obj.get_status_display(),
        )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'order',
        'product_image',
        'product',
        'quantity',
        'price',
        'item_total',
    )

    search_fields = (
        'product__name',
        'order__name',
        'order__email',
    )

    list_filter = (
        'product',
    )

    readonly_fields = (
        'item_total',
    )

    ordering = (
        '-id',
    )

    list_per_page = 20

    @admin.display(description='Image')
    def product_image(self, obj):
        if obj.product and obj.product.image:
            return format_html(
                '<img src="{}" width="60" height="60" '
                'style="object-fit:cover; border-radius:8px;" />',
                obj.product.image.url,
            )

        return 'No Image'