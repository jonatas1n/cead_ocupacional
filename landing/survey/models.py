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

    name = models.CharField(verbose_name="Nome", null=True, blank=True, max_length=50)
    function = models.CharField(verbose_name="Função", null=True, blank=True, max_length=255)
    phone = models.CharField(verbose_name='Telefone', null=True, blank=True, max_length=255)
    email = models.CharField(verbose_name="E-mail da empresa", null=True, blank=True, max_length=255)
    birthday = models.DateField(verbose_name='Data de nascimento', blank=True, null=True)
    rg = models.CharField(verbose_name="RG", null=True, blank=True, max_length=255)
    cpf = models.CharField(verbose_name="CPF", null=True, blank=True, max_length=11)
    social_reason = models.CharField(verbose_name="Razão Social", null=True, blank=True, max_length=255)
    toxicologic = models.CharField(verbose_name="Toxicológico?", null=True, blank=True, max_length=1)
    contract_type = models.CharField(verbose_name="Tipo de contrato", null=True, blank=True, max_length=255)
    cnpj = models.CharField(verbose_name="CNPJ", null=True, blank=True, max_length=30)
    exam_type = models.CharField(verbose_name='Tipo de exame', null=True, blank=True, max_length=255)

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("hour"),
    ]

    def __str__(self):
        f"{self.hour} | {self.date}"
