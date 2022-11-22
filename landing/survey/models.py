from django.db import models
from wagtail.core.fields import StreamField
from wagtailstreamforms.blocks import WagtailFormBlock
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtailmetadata.models import MetadataPageMixin
from wagtail.core.models import Page
from wagtail.core import blocks

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
    toxicologic = models.CharField(verbose_name="Toxicológico?", null=True, blank=True, max_length=3)
    contract_type = models.CharField(verbose_name="Tipo de contrato", null=True, blank=True, max_length=255)
    cnpj = models.CharField(verbose_name="CNPJ", null=True, blank=True, max_length=30)
    exam_type = models.CharField(verbose_name='Tipo de exame', null=True, blank=True, max_length=255)

    rac_form = StreamField([
        ("rac_forms",
            blocks.ChoiceBlock(label='Formulários RAC', choices=[
                ("rac_1", "RAC 1"),
                ("rac_2", "RAC 2"),
                ("rac_3", "RAC 3"),
                ("rac_4", "RAC 4"),
                ("rac_5", "RAC 5"),
                ("rac_6", "RAC 6"),
                ("rac_7", "RAC 7"),
                ("rac_8", "RAC 8"),
                ("rac_9", "RAC 9"),
                ("rac_10", "RAC 10"),
                ("rac_11", "RAC 11"),
                ("rac_12", "RAC 12"),
            ])
        )
    ], null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("hour"),
        FieldPanel('name'),
        FieldPanel('function'),
        FieldPanel('phone'),
        FieldPanel('email'),
        FieldPanel('birthday'),
        FieldPanel('rg'),
        FieldPanel('cpf'),
        FieldPanel('social_reason'),
        FieldPanel('toxicologic'),
        FieldPanel('contract_type'),
        FieldPanel('cnpj'),
        FieldPanel('exam_type'),
        StreamFieldPanel('rac_form'),
    ]

    def __str__(self):
        f"{self.hour} | {self.date}"

class SurveyPageIndex(Page):

    def get_context(self, request):
        context = super(SurveyPageIndex, self).get_context(request)
        context['schedules'] = list(SurveyPage.objects.all())
        return context

class SchedulingPage(Page):
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
