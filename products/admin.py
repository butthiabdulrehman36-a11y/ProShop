from django.contrib import admin
from django.utils.html import format_html

from .models import Product


def admin_product_image_url(image):
    if not image:
        return ""

    name = image.name

    if name.startswith("products/"):
        return f"/static/{name}"

    return image.url


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'image_thumbnail',
        'name',
        'formatted_price',
        'stock_status',
        'formatted_date',
    )

    list_display_links = (
        'name',
    )

    search_fields = (
        'name',
        'description',
    )

    list_filter = (
        'stock',
        'created_at',
    )

    ordering = (
        'name',
    )

    list_per_page = 10

    readonly_fields = (
        'created_at',
        'image_preview',
    )

    fieldsets = (
        (
            'Product Information',
            {
                'fields': (
                    'name',
                    'description',
                    'price',
                ),
            },
        ),
        (
            'Inventory & Image',
            {
                'fields': (
                    'stock',
                    'image',
                    'image_preview',
                    'created_at',
                ),
            },
        ),
    )

    @admin.display(description='Image')
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" '
                'style="object-fit: cover; border-radius: 6px;" />',
                admin_product_image_url(obj.image),
            )

        return 'No Image'

    @admin.display(description='Current Image')
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="200" '
                'style="object-fit: contain; border-radius: 8px;" />',
                admin_product_image_url(obj.image),
            )

        return 'No Image'

    @admin.display(
        description='Price',
        ordering='price',
    )
    def formatted_price(self, obj):
        return f'PKR {obj.price:,.2f}'

    @admin.display(
        description='Stock',
        ordering='stock',
    )
    def stock_status(self, obj):
        if obj.stock > 0:
            return format_html(
                '<span style="display:inline-block; '
                'color:white; '
                'background:#22c55e; '
                'padding:5px 10px; '
                'border-radius:15px; '
                'font-weight:bold; '
                'font-size:13px; '
                'white-space:nowrap;">'
                '{} Available'
                '</span>',
                obj.stock,
            )

        return format_html(
            '<span style="display:inline-block; '
            'color:white; '
            'background:#ef4444; '
            'padding:5px 10px; '
            'border-radius:15px; '
            'font-weight:bold; '
            'font-size:13px; '
            'white-space:nowrap;">'
            '{}'
            '</span>',
            'Out of Stock',
        )

    @admin.display(
        description='Created',
        ordering='created_at',
    )
    def formatted_date(self, obj):
        return obj.created_at.strftime(
            '%d-%m-%Y %I:%M %p'
        )
