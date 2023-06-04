from slugify import slugify


def to_slug(text):
    return slugify(text, separator="-")
