"""
Wagtail API v2 configuration.
Exposes property list at /api/v2/propertys/
"""
from rest_framework.filters import BaseFilterBackend
from wagtail.api.v2.utils import BadRequestError
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter

from website.models import PropertyPage


api_router = WagtailAPIRouter("wagtailapi")


class ExtendedFilteringBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # Define which fields you want to allow range filtering on
        # For your property app, this might be 'price' or 'sqft'
        range_fields = ['price', 'sqft', 'bedrooms']

        for field in range_fields:
            # Look for __gt, __lt, __gte, __lte in the URL parameters
            for lookup in ['__gt', '__lt', '__gte', '__lte']:
                param = f"{field}{lookup}"
                value = request.GET.get(param)

                if value:
                    try:
                        # Apply the Django filter dynamically
                        queryset = queryset.filter(**{param: value})
                    except ValueError:
                        raise BadRequestError(f"Invalid value for {param}")

        return queryset


class PropertysAPIViewSet(PagesAPIViewSet):
    """API endpoint for PropertyPage list and detail."""

    model = PropertyPage
    name = "propertys"
    filter_backends = PagesAPIViewSet.filter_backends + [ExtendedFilteringBackend]
    known_query_parameters = PagesAPIViewSet.known_query_parameters | {
        'price__gt', 'price__lt', 'price__gte', 'price__lte',
        'sqft__gte', 'sqft__lte', 'bedrooms__gte', 'bedrooms__lte',
    }


api_router.register_endpoint("propertys", PropertysAPIViewSet)
