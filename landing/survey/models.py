from tabnanny import verbose
from django.db import models
from wagtail.core.fields import StreamField
from wagtailstreamforms.blocks import WagtailFormBlock
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtailmetadata.models import MetadataPageMixin
from wagtail.core.models import Page


class SurveyPageIndex(Page):
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

    def get_context(self, request):
        context = super(SurveyPageIndex, self).get_context(request)
        return context


class SurveyPage(MetadataPageMixin, Page):
    date = models.DateField(blank=False, null=False)
    hour = models.TimeField(blank=False, null=False)

    survey = models.ForeignKey(
        "wagtailstreamforms.FormSubmission",
        verbose_name=("Enquete"),
        on_delete=models.CASCADE,
    )

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("hour"),
        FieldPanel("survey"),
    ]
