from django.utils.text import slugify


def generate_unique_slug(model, value, slug_field='slug'):
    """
    Generates a unique slug for any model.
    Example:
        drake
        drake-1
        drake-2
    """

    base_slug = slugify(value)
    slug = base_slug
    counter = 1

    while model.objects.filter(**{slug_field: slug}).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug