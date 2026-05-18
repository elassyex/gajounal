"""
Create or customize your page models here.
"""

from coderedcms.blocks import NAVIGATION_STREAMBLOCKS, BaseBlock
from coderedcms.fields import CoderedStreamField
from django.db import models
from django.db.models import Q
from modelcluster.fields import ParentalKey
from coderedcms.forms import CoderedFormField
from coderedcms.models import (
    CoderedArticlePage,
    CoderedArticleIndexPage,
    CoderedEmail,
    CoderedFormPage,
    CoderedWebPage,
)
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.api import APIField
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import StreamField
from wagtail.images import get_image_model_string
from wagtail.images.api.fields import ImageRenditionField
from wagtail.models import TranslatableMixin, Orderable
from wagtail.snippets.models import register_snippet

from website.blocks import CUSTOM_CONTENT_STREAMBLOCKS, CUSTOM_LAYOUT_STREAMBLOCKS


class ArticlePage(CoderedArticlePage):
    """
    Article, suitable for news or blog content.
    """

    class Meta:
        verbose_name = "Article"
        ordering = ["-first_published_at"]

    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ["website.ArticleIndexPage"]

    template = "coderedcms/pages/article_page.html"
    search_template = "coderedcms/pages/article_page.search.html"

    body = StreamField(
        CUSTOM_CONTENT_STREAMBLOCKS,
        null=True,
        blank=True,
        use_json_field=True,
    )


class ArticleIndexPage(CoderedArticleIndexPage):
    """
    Shows a list of article sub-pages.
    """

    class Meta:
        verbose_name = "Article Landing Page"

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "website.ArticlePage"

    # Only allow ArticlePages beneath this page.
    subpage_types = ["website.ArticlePage"]

    template = "coderedcms/pages/article_index_page.html"

    body = StreamField(
        CUSTOM_LAYOUT_STREAMBLOCKS,
        null=True,
        blank=True,
        use_json_field=True,
    )


class HomePage(CoderedWebPage):
    """
    Home page for the estate agent website.
    """

    class Meta:
        verbose_name = "Home Page"

    template = "coderedcms/pages/home_page.html"

    body = StreamField(
        CUSTOM_LAYOUT_STREAMBLOCKS,
        null=True,
        blank=True,
        use_json_field=True,
    )


class LocationPage(CoderedArticlePage):
    class Meta:
        verbose_name = "Location"
        ordering = ["-first_published_at"]

    parent_page_types = ["website.LocationIndexPage"]
    template = "coderedcms/pages/location_page.html"
    search_template = "coderedcms/pages/location_page.search.html"

    body = StreamField(
        CUSTOM_LAYOUT_STREAMBLOCKS,
        null=True,
        blank=True,
        use_json_field=True,
    )

    address = models.CharField(max_length=255, blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    thumbnail = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Thumbnail image",
    )

    content_panels = CoderedArticlePage.content_panels + [
        FieldPanel("address"),
        FieldPanel("tel"),
        FieldPanel("thumbnail"),
    ]


class LocationIndexPage(CoderedArticleIndexPage):
    class Meta:
        verbose_name = "Location Landing Page"

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "website.LocationPage"

    # Only allow ArticlePages beneath this page.
    subpage_types = ["website.LocationPage"]

    template = "coderedcms/pages/location_index_page.html"

    body = StreamField(
        CUSTOM_LAYOUT_STREAMBLOCKS,
        null=True,
        blank=True,
        use_json_field=True,
    )


class PropertyPage(CoderedArticlePage):
    class Meta:
        verbose_name = "Property"
        ordering = ["-first_published_at"]

    parent_page_types = ["website.PropertyIndexPage"]
    template = "coderedcms/pages/property_page.html"
    search_template = "coderedcms/pages/property_page.search.html"

    body = StreamField(
        CUSTOM_LAYOUT_STREAMBLOCKS,
        null=True,
        blank=True,
        use_json_field=True,
    )

    address = models.CharField(max_length=255, blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    thumbnail = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Thumbnail image",
    )

    # Filter fields
    bedrooms = models.PositiveIntegerField(blank=True, null=True, verbose_name="Bedrooms")
    property_type = models.CharField(choices=[("house", "House"), ("flat", "Flat"), ("apartment", "Apartment")],
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Type",
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        blank=True,
        null=True,
        help_text="Price (filter uses min/max range)",
    )
    bathrooms = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Bathrooms",
    )
    sqft = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Square Footage",
    )
    parking_spaces = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Parking Spaces",
    )
    has_garden = models.BooleanField(default=False)
    has_balcony = models.BooleanField(default=False)
    energy_rating = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="Energy Rating (e.g., A, B)",
    )
    year = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Build Year",
        help_text="Build year",
    )
    refit_year = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Refit Year",
    )
    reception_rooms = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Reception Rooms",
    )

    is_sold = models.BooleanField(default=False)
    sold_time = models.DateTimeField(blank=True, null=True)
    is_feature = models.BooleanField(default=False)

    content_panels = CoderedArticlePage.content_panels + [
        FieldPanel("address"),
        FieldPanel("tel"),
        FieldPanel("thumbnail"),
        FieldPanel("bedrooms"),
        FieldPanel("property_type"),
        FieldPanel("price"),
        FieldPanel("bathrooms"),
        FieldPanel("sqft"),
        FieldPanel("parking_spaces"),
        FieldPanel("has_garden"),
        FieldPanel("has_balcony"),
        FieldPanel("energy_rating"),
        FieldPanel("year"),
        FieldPanel("refit_year"),
        FieldPanel("reception_rooms"),
        FieldPanel("is_sold"),
        FieldPanel("sold_time"),
        FieldPanel("is_feature"),
        InlinePanel("gallery_images", heading="Gallery", label="Gallery image"),
    ]

    api_fields = [
        APIField("body"),
        APIField("address"),
        APIField("tel"),
        APIField("thumbnail"),
        APIField(
            "thumbnail_card",
            serializer=ImageRenditionField("fill-800x450", source="thumbnail"),
        ),
        APIField("bedrooms"),
        APIField("property_type"),
        APIField("price"),
        APIField("bathrooms"),
        APIField("sqft"),
        APIField("parking_spaces"),
        APIField("has_garden"),
        APIField("has_balcony"),
        APIField("energy_rating"),
        APIField("year"),
        APIField("refit_year"),
        APIField("reception_rooms"),
        APIField("is_sold"),
        APIField("sold_time"),
        APIField("is_feature"),
    ]


class PropertyPageGalleryImage(Orderable, models.Model):
    page = ParentalKey(
        PropertyPage,
        on_delete=models.CASCADE,
        related_name="gallery_images",
    )
    image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    caption = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
    ]


class PropertyIndexPage(CoderedArticleIndexPage):


class CupcakesIndexPage(CoderedWebPage):
    """Placeholder for the original Cupcakes index page type."""
    class Meta:
        verbose_name = "Cupcakes Index Page"

    # Allow only CupcakesPage as a child.
    subpage_types = ["website.CupcakesPage"]
    template = "coderedcms/pages/web_page.html"


class CupcakesPage(CoderedWebPage):
    """Placeholder for individual cupcake pages."""
    class Meta:
        verbose_name = "Cupcakes Page"

    template = "coderedcms/pages/web_page.html"
    class Meta:
        verbose_name = "Property Landing Page"

    index_query_pagemodel = "website.PropertyPage"
    subpage_types = ["website.PropertyPage"]

    template = "coderedcms/pages/property_index_page.html"

    body = StreamField(
        CUSTOM_LAYOUT_STREAMBLOCKS,
        null=True,
        blank=True,
        use_json_field=True,
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        properties = self.get_index_children().live().specific()
        
        # Keyword search (title + address)
        query = request.GET.get("q", "").strip()
        if query:
            properties = properties.filter(
                Q(title__icontains=query) | Q(address__icontains=query)
            )

        # Bed filter
        min_beds = request.GET.get("min_beds")
        if min_beds and min_beds.isdigit():
            properties = properties.filter(bedrooms__gte=int(min_beds))

        # Price filter
        min_price = request.GET.get("min_price")
        if min_price and min_price.isdigit():
            properties = properties.filter(price__gte=int(min_price))
        max_price = request.GET.get("max_price")
        if max_price and max_price.isdigit():
            properties = properties.filter(price__lte=int(max_price))

        # Type filter
        prop_type = request.GET.get("property_type")
        if prop_type:
            properties = properties.filter(property_type=prop_type)
            
        context['index_paginated'] = properties
        return context


class FormPage(CoderedFormPage):
    """
    A page with an html <form>.
    """

    class Meta:
        verbose_name = "Form"

    template = "coderedcms/pages/form_page.html"


class FormPageField(CoderedFormField):
    """
    A field that links to a FormPage.
    """

    class Meta:
        ordering = ["sort_order"]

    page = ParentalKey("FormPage", related_name="form_fields")


class FormConfirmEmail(CoderedEmail):
    """
    Sends a confirmation email after submitting a FormPage.
    """

    page = ParentalKey("FormPage", related_name="confirmation_emails")


class WebPage(CoderedWebPage):
    """
    General use page with featureful streamfield and SEO attributes.
    """

    class Meta:
        verbose_name = "Web Page"

    template = "coderedcms/pages/web_page.html"

    body = StreamField(
        CUSTOM_LAYOUT_STREAMBLOCKS,
        null=True,
        blank=True,
        use_json_field=True,
    )


@register_snippet
class TranslateNavbar(TranslatableMixin, models.Model):
    """
    Snippet for site navigation bars (header, main menu, etc.)
    """
    name = models.CharField(
        max_length=255,
        verbose_name="Name",
    )
    custom_css_class = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Custom CSS Class",
    )
    custom_id = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Custom ID",
    )
    menu_items = CoderedStreamField(
        NAVIGATION_STREAMBLOCKS,
        verbose_name="Navigation links",
        blank=True,
        use_json_field=True,
    )

    panels = [
        FieldPanel("name"),
        MultiFieldPanel(
            [
                FieldPanel("custom_css_class"),
                FieldPanel("custom_id"),
            ],
            heading="Attributes",
        ),
        FieldPanel("menu_items"),
    ]

    def __str__(self):
        return self.name


@register_setting(icon="cr-desktop")
class CustomSetting(ClusterableModel, BaseSiteSetting):
    """
    Tracking and Google Analytics.
    """

    class Meta:
        verbose_name = "Custom Settings"

    captcha = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="captcha key",
        help_text='Your captcha site key'
        ,
    )
    language_menu = models.BooleanField(
        default=True,
        verbose_name="language menu item",
        help_text="Show/hide language menu item"
    )
    content_margin_top = models.IntegerField(
        default=0,
        verbose_name="content margin top (px)",
        help_text="margin top for content, use with fixed navbar settings"
    )
    footer_bg_color = models.CharField(
        null=True, blank=True, max_length=500,
        verbose_name="footer background color",
        help_text="footer background color value"
    )
    footer_text_color = models.CharField(
        null=True, blank=True, max_length=500,
        verbose_name="Footer text color",
        help_text="Footer text color value"
    )
    nav_bg_color = models.CharField(
        null=True, blank=True, max_length=500,
        verbose_name="Navbar background color",
        help_text="Navbar background color value"
    )

    facebook_page_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="facebook page id",
        help_text='Your facebook page id',
    )

    using_messenger = models.BooleanField(
        default=True,
        verbose_name="using facebook messenger chat support",
        help_text="Show/hide facebook messenger chat support"
    )

    whatsapp_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="whatsapp id",
        help_text='Your whatsapp id',
    )

    using_whatsapp = models.BooleanField(
        default=True,
        verbose_name="using whatsapp chat support",
        help_text="Show/hide whatsapp chat support"
    )
    email_host = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="EMAIL_HOST",
        help_text='Your Email Host',
    )
    email_port = models.PositiveIntegerField(
        default=0,
        verbose_name="EMAIL_PORT",
        help_text='Your Email Port',
    )
    email_use_tls = models.BooleanField(
        default=True,
        verbose_name="EMAIL_USE_TLS",
        help_text='Your Email Use TLS',
    )
    email_host_user = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="EMAIL_HOST_USER",
        help_text="Your Email Host User"
    )
    email_host_password = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="EMAIL_HOST_PASSWORD",
        help_text='Your Email Host Password',
    )
    email_sender = models.EmailField(
        null=True,
        verbose_name="Email Sender",
        help_text="Your email sender"
    )
    owner_mail = models.EmailField(
        null=True,
        verbose_name="Owner Mail",
        help_text="Owner Mail"
    )

    custom_css = models.TextField(
        null=True,
        verbose_name="Custom CSS",
        help_text="Custom CSS"
    )
    panels = [
        FieldPanel("captcha"),
        FieldPanel("language_menu"),
        FieldPanel("content_margin_top"),
        FieldPanel("nav_bg_color"),
        FieldPanel("footer_bg_color"),
        FieldPanel("footer_text_color"),
        FieldPanel("facebook_page_id"),
        FieldPanel("using_messenger"),
        FieldPanel("whatsapp_id"),
        FieldPanel("using_whatsapp"),
        FieldPanel("email_host"),
        FieldPanel("email_port"),
        FieldPanel("email_use_tls"),
        FieldPanel("email_host_user"),
        FieldPanel("email_host_password"),
        FieldPanel("email_sender"),
        FieldPanel("owner_mail"),

        InlinePanel(
            "site_navbartrans",
            help_text="Choose one or more navbars for your site.",
            heading="Site Navbars",
        ),
        FieldPanel("custom_css"),
    ]


class TransNavbarOrderable(Orderable, models.Model):
    navbar_chooser = ParentalKey(
        CustomSetting,
        related_name="site_navbartrans",
        verbose_name="Site Navbars",
    )
    navbar = models.ForeignKey(
        TranslateNavbar,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    panels = [FieldPanel("navbar")]


@register_snippet
class LocationMarker(models.Model):
    location = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    tel = models.CharField(max_length=20, help_text="Enter phone number in the format +1234567890")
    description = models.CharField(max_length=255, default='', verbose_name="Address")
    link = models.URLField(blank=True, null=True, help_text="Enter a link associated with this location")

    panels = [
        FieldPanel('location'),
        FieldPanel('latitude'),
        FieldPanel('longitude'),
        FieldPanel('tel'),
        FieldPanel('description'),
        FieldPanel('link'),
    ]

    def __str__(self):
        return self.location

    class Meta:
        verbose_name = "Location Marker"
YachtPage = PropertyPage
YachtIndexPage = PropertyIndexPage
