from wagtail.core.models import Page
from django.db import models

from wagtailmetadata.models import MetadataPageMixin
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.core.blocks import (
    BooleanBlock,
    TextBlock,
    StructBlock,
    CharBlock,
    URLBlock,
    ChoiceBlock
)
from wagtail.images.blocks import ImageChooserBlock


class LandingPage(MetadataPageMixin, Page):
    is_creatable = False

    ads = StreamField(
        [
            (
                "ad",
                StructBlock(
                    [
                        ("text", CharBlock(label="Texto do anúncio", required=False)),
                        (
                            "image",
                            ImageChooserBlock(label="Imagem do anúncio", required=True),
                        ),
                        ("link", URLBlock(label="Link", required=False)),
                    ]
                ),
            )
        ],
        null=True,
        blank=True,
    )

    scheduling_btn_text = models.CharField(
        null=False, blank=False, default="Realizar agendamento", max_length=256
    )

    scheduling_subtext = models.CharField(null=True, blank=True, max_length=256)

    popup = StreamField(
        [
            (
                "popup",
                StructBlock(
                    [
                        ("active", BooleanBlock(label="Ativo", required=False)),
                        ("title", CharBlock(label="Título", required=False)),
                        ("text", TextBlock(label="Texto do popup", required=False)),
                    ],
                    max_num=1,
                    required=False,
                ),
            )
        ],
        max_num=1,
        null=True,
        blank=True,
    )

    social_media = StreamField(
        [
            (
                "social_media",
                StructBlock(
                    [
                        ("service", ChoiceBlock(label="Rede Social", choices=[
                            ("instagram", "Instagram"),
                            ("facebook", "Facebook"),
                            ("twitter", "Twitter"),
                        ])),
                        ("link", URLBlock(label="Link")),
                    ]
                ),
            )
        ],
        null=True,
        blank=True,
    )

    def get_context(self, request):
        context = super(LandingPage, self).get_context(request)
        context["days"] = [29, 30, 31] + list(range(1, 32)) + [1]
        context["social_media"] = self.social_media
        return context

    content_panels = Page.content_panels + [
        StreamFieldPanel("ads"),
        FieldPanel("scheduling_btn_text"),
        FieldPanel("scheduling_subtext"),
        StreamFieldPanel("social_media"),
        StreamFieldPanel("popup"),
    ]

class ReturnPage(Page):
    is_creatable = False
    pass

class Contact(Page):
    pass