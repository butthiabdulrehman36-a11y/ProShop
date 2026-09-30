from django import template

register = template.Library()


@register.filter
def product_image_url(image):
    if not image:
        return ""

    name = image.name

    if name.startswith("products/"):
        return f"/static/{name}"

    return image.url
