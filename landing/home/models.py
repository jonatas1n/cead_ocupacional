from wagtail.core.models import Page
from django.db import models

from wagtailmetadata.models import MetadataPageMixin
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtailstreamforms.blocks import WagtailFormBlock
from wagtail.core.blocks import BooleanBlock, TextBlock, StructBlock, CharBlock, URLBlock
from wagtail.images.blocks import ImageChooserBlock

class LandingPage(MetadataPageMixin, Page):
    is_creatable = False

    ads = StreamField([
        ("ad", StructBlock([
            ("text", CharBlock(label="Texto do anúncio", required=False)),
            ("image", ImageChooserBlock(label="Imagem do anúncio", required=True)),
            ("link", URLBlock(label="Link", required=False))
        ]))
    ], null=True, blank=True)

    schedulling_btn_text = models.CharField(null=False, blank=False, default="Realizar agendamento", max_length=256)

    schedulling_subtext = models.CharField(null=True, blank=True, max_length=256)

    popup = StreamField([
        ("popup", StructBlock([
            ("active", BooleanBlock(label="Ativo", required=False)),
            ("title", CharBlock(label="Título", required=False)),
            ("text", TextBlock(label="Texto do popup", required=False))
        ], max_num=1, required=False))
    ], max_num=1, null=True, blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel("ads"),
        StreamFieldPanel("popup"),
        FieldPanel("schedulling_btn_text"),
        FieldPanel("schedulling_subtext")
    ]

class SurveysPage(MetadataPageMixin, Page):
    surveys = StreamField(
        [
            ("form", WagtailFormBlock()),
        ],
        blank=True,
        null=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("surveys"),
    ]
