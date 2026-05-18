"""
Views for website app.
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from wagtail.models import Page

from website.models import PropertyPage


@require_GET
def property_gallery_api(request, page_id):
    """
    API endpoint: GET /api/v2/property-gallery/<page_id>/
    Returns JSON: { "gallery": [ {"url": "...", "caption": "..."}, ... ] }
    """
    try:
        page = Page.objects.get(pk=page_id).specific
    except (Page.DoesNotExist, Page.MultipleObjectsReturned):
        return JsonResponse({"gallery": []}, status=404)

    if not isinstance(page, PropertyPage):
        return JsonResponse({"gallery": []}, status=404)

    gallery = []
    for item in page.gallery_images.all():
        if not item.image:
            continue
        thumb_rendition = item.image.get_rendition("fill-400x300")
        thumb_url = request.build_absolute_uri(thumb_rendition.url)
        full_url = request.build_absolute_uri(item.image.file.url)
        gallery.append({
            "url": thumb_url,
            "url_full": full_url,
            "caption": item.caption or "",
        })

    return JsonResponse({"gallery": gallery})
