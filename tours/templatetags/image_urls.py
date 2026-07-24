from urllib.parse import urlsplit

from django import template
from django.templatetags.static import static


register = template.Library()

DEFAULT_WIDTH = 800
MIN_WIDTH = 64
MAX_WIDTH = 2400

TOUR_FALLBACK_IMAGES = {
    "3-day-kibale-chimpanzee-experience": (
        "images/tours/kibale-chimpanzee.jpg"
    ),
    "5-day-gorilla-and-queen-elizabeth-safari": (
        "images/tours/bwindi-gorillas.jpg"
    ),
    "5-day-kidepo-valley-wilderness-safari": (
        "images/tours/kidepo-valley.jpg"
    ),
    "7-day-western-uganda-wildlife-and-primates": (
        "images/tours/western-uganda-hippos.jpg"
    ),
    "10-day-uganda-grand-safari": (
        "images/tours/lake-mburo-zebras.jpg"
    ),
    "3-day-bwindi-gorilla-trekking": (
        "images/tours/bwindi-gorillas.jpg"
    ),
    "2-day-lake-mburo-safari": (
        "images/tours/lake-mburo-zebras.jpg"
    ),
}


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


@register.simple_tag
def tour_image_url(tour, width=DEFAULT_WIDTH):
    """Return a tour's uploaded image or a curated local fallback."""
    if not tour:
        return ""

    uploaded_url = optimized_image_url(
        getattr(tour, "image", None),
        width,
    )
    if uploaded_url:
        return uploaded_url

    fallback_path = TOUR_FALLBACK_IMAGES.get(
        getattr(tour, "slug", ""),
    )
    if not fallback_path:
        return ""

    return static(fallback_path)


@register.simple_tag(takes_context=True)
def absolute_tour_image_url(context, tour, width=1600):
    """Return an absolute uploaded or fallback tour image URL."""
    url = tour_image_url(tour, width)
    if not url:
        return ""

    if url.startswith(("https://", "http://")):
        return url

    request = context.get("request")
    if request is None:
        return url

    return request.build_absolute_uri(url)
