from django import template

register = template.Library()


@register.filter
def product_image_url(image):
    if not image:
        return ""

    return image.url
