from urllib.parse import urlsplit

from django import template


register = template.Library()

DEFAULT_WIDTH = 800
MIN_WIDTH = 64
MAX_WIDTH = 2400


@register.filter
def optimized_image_url(image, width=DEFAULT_WIDTH):
    """Return an optimized Cloudinary URL or the original media URL."""
    if not image:
        return ""

    try:
        url = image.url
    except (AttributeError, ValueError):
        return ""

    try:
        requested_width = int(width)
    except (TypeError, ValueError):
        requested_width = DEFAULT_WIDTH

    requested_width = max(
        MIN_WIDTH,
        min(requested_width, MAX_WIDTH),
    )

    cloudinary_marker = "/image/upload/"
    parsed_url = urlsplit(url)

    if (
        parsed_url.hostname != "res.cloudinary.com"
        or cloudinary_marker not in url
    ):
        return url

    transformation = (
        f"c_limit,w_{requested_width}/f_auto/q_auto/"
    )

    return url.replace(
        cloudinary_marker,
        f"{cloudinary_marker}{transformation}",
        1,
    )


@register.simple_tag(takes_context=True)
def absolute_optimized_image_url(
    context,
    image,
    width=1600,
):
    """Return an absolute optimized URL for social-sharing metadata."""
    url = optimized_image_url(image, width)
    if not url:
        return ""

    if url.startswith(("https://", "http://")):
        return url

    request = context.get("request")
    if request is None:
        return url

    return request.build_absolute_uri(url)
