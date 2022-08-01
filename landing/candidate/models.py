from django.db import models
from django.db.models.signals import post_save
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.dispatch import receiver
from django.template.defaultfilters import slugify

from wagtailmetadata.models import MetadataPageMixin
from wagtail.core.models import Page
from wagtail.search import index
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtailstreamforms.models import FormSubmission

from wagtail.core.blocks import StructBlock, ChoiceBlock, URLBlock
from django.db.models import CharField, ImageField, EmailField, URLField, DateField
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests


from candidate.util import uf_list, subject_dict, subject_descriptions, subjects_list
from candidate.factories import SurveyCandidateFactory

class CandidatePage(MetadataPageMixin, Page):
    DEPUTADO_CHARGE_TEXT = "Deputado(a) Federal"
    id_autor = models.IntegerField(blank=True, null=True, unique=True)
    id_parlametria = models.IntegerField(blank=True, null=True, unique=True)
    id_serenata = models.IntegerField(blank=True, null=True, unique=True)

    parent_page_types = [
        "candidate.CandidateIndexPage",
    ]

    search_fields = Page.search_fields + [
        index.SearchField("id_autor"),
        index.FilterField("title"),
    ]

    campaign_name = CharField(null=True, max_length=255)
    party = CharField(null=True, blank=True, max_length=255)
    cpf = CharField(max_length=14, null=True)
    birth_date = DateField(blank=True, null=True)
    email = EmailField(null=True)
    picture = ImageField(null=True, blank=True, default=None)
    charge = CharField(null=True, max_length=255)
    social_media = StreamField([
        ('twitter', URLBlock(max_length=255)),
        ('facebook', URLBlock(max_length=255)),
        ('instagram', URLBlock(max_length=255)),
        ('youtube', URLBlock(max_length=255)),
    ], null=True, blank=True)

    manager_name = CharField(null=True, max_length=255)
    manager_email = EmailField(null=True)
    manager_phone = CharField(max_length=50, null=True)
    manager_site = URLField(null=True, blank=True)

    election_state = CharField(null=True, max_length=255)
    election_city = CharField(null=True, max_length=255)

    global make_block

    def make_block(subject):
        _, phrase, key = subject.values()
        choices = [
            ("Sim", "Sim"),
            ("Não", "Não"),
            ("Prefiro não responder / Não sei", "Prefiro não responder / Não sei"),
        ]

        return (
            key,
            ChoiceBlock(
                choices=choices,
                defult=True,
                label=f'Opinião do candidato em relação à frase "{phrase}."',
            ),
        )

    opinions = StreamField(
        [
            (
                "opinions",
                StructBlock(
                    [make_block(subject) for subject in subjects_list],
                ),
            )
        ],
        null=True,
    )

    @property
    def opinions_answers(self):
        answers = subjects_list
        answer_dict = {
            "Sim": "sim",
            "Não": "nao",
            "Prefiro não responder / Não sei": "nao_sei",
        }
        phrase_dict = {
            "Sim": "É",
            "Não": "Não é",
            "Prefiro não responder / Não sei": "Não declarei minha opinião sobre ser",
        }
        opinions = self.opinions[0].value
        for key, answer in enumerate(answers):
            answer_key = opinions[answer["key"]]
            answers[key]["phrase"] = answers[key]["phrase"].replace(
                "Sou", phrase_dict[answer_key]
            )
            answers[key]["answer"] = answer_dict[answer_key]
        return answers

    @property
    def get_picture(self):
        if self.picture:
            return self.picture.url

        if self.id_autor:
            return self._get_external_picture_link()

        return ""


    def _get_external_picture_link(self):
        senador_picture_url = "https://www.senado.leg.br/senadores/img/fotos-oficiais/senador"
        deputado_picture_url = "https://www.camara.leg.br/internet/deputado/bandep/"

        if self.charge == "Senador(a)":
            return f"{senador_picture_url}{self.id_autor}.jpg"
        return f"{deputado_picture_url}{self.id_autor}.jpg"


    @property
    def is_deputado(self) -> bool:
        return self.charge == self.DEPUTADO_CHARGE_TEXT

    @property
    def is_senador(self) -> bool:
        return not self.is_deputado

    @property
    def adhesion(self):
        response = requests.get(
            "https://demo3265586.mockable.io/farol-verde/votacoes/parlamentar/33223"
        )
        response = response.json()
        return response["adhesion"]

    @property
    def discipline(self):
        try:
            response = requests.get(f'https://api.parlametria.org.br/disciplina/{self.id_parlametria}')
            response = response.json()
            response = response[0]['disciplina']
            if response is None:
                response = 0
            response *= 100
            return f'{response:,.2f}%'
        except:
            return None

    @property
    def governism(self):
        try:
            response = requests.get(f'https://api.parlametria.org.br/governismo/{self.id_parlametria}')
            response = response.json()
            response = response[0]['governismo']
            if response is None:
                response = 0
            response = (response + 10) * 5

            return f'{response:,.2f}%'
        except:
            return None

    def get_propositions(self):
        response = requests.get(
            "https://demo3265586.mockable.io/farol-verde/votacoes/parlamentar/33223"
        )
        response = response.json()
        propositions = response["propositions"]
        return Paginator(propositions, 10)

    def get_context(self, request):
        context = super().get_context(request)
        page = request.GET.get("page", 1)
        propositions = self.get_propositions()
        total_propositions = propositions.count
        try:
            propositions = propositions.page(page)
        except EmptyPage:
            propositions = propositions.page(propositions.num_pages)
        context["propositions"] = propositions
        context["total_propositions"] = total_propositions
        return context

    content_panels = Page.content_panels + [
        FieldPanel("id_autor", classname="full"),
        FieldPanel("id_parlametria", classname="full"),
        FieldPanel("id_serenata", classname="full"),
        FieldPanel('campaign_name'),
        FieldPanel('party'),
        FieldPanel('cpf'),
        FieldPanel('birth_date'),
        FieldPanel('email'),
        FieldPanel('picture'),
        FieldPanel('charge'),
        StreamFieldPanel('social_media'),
        FieldPanel('manager_name'),
        FieldPanel('manager_email'),
        FieldPanel('manager_phone'),
        FieldPanel('manager_site'),
        FieldPanel('election_state'),
        FieldPanel('election_city'),
        StreamFieldPanel('opinions'),
    ]

    def __str__(self):
        return f"{self.id_autor}: {self.title}"


class CandidateIndexPage(MetadataPageMixin, Page):
    ajax_template = 'candidate/candidate_index_ajax.html'

    parent_page_types = [
        "home.LandingPage",
    ]

    subpage_types = [
        "candidate.CandidatePage",
    ]

    description = models.CharField(
        max_length=255,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("description", classname="full"),
    ]

    def search_results(self, request):
        queryset = CandidatePage.objects.order_by('title')

        charges_dict = {'senators': 'Senador(a)', 'deputies': 'Deputado(a) Federal'}
        charges = []

        params_functions = {
            'name': lambda queryset, value: queryset.filter(title__icontains=value),
            'uf[]': lambda queryset, values: queryset.filter(election_state__in=values),
            'party[]': lambda queryset, values: queryset.filter(party__in=values),
            'sortby': lambda queryset, value: queryset.order_by('-title') if value == 'descending' else queryset,
        }

        request_items = dict(request.GET)
        for param, value in list(request_items.items()):
            if param in charges_dict.keys():
                charges.append(charges_dict[param])
            if param not in ['uf[]', 'party[]']:
                value = value[0]
            if value and param in params_functions:
                queryset = params_functions[param](queryset, value)

        return queryset.filter(charge__in=charges)


    def get_context(self, request):
        context = super(CandidateIndexPage, self).get_context(request)

        search_results = self.search_results(request)
        search_results = search_results.filter(live=True) # do not display draft pages
        subject = request.GET.get('subject', None)
        candidates_opinions = [''] * len(search_results)

        if subject:
            candidates_opinions = [
                candidate.opinions[0].value.get(subject_dict[subject])
                for candidate in search_results
            ]
            context["subject_description"] = (
                subject_descriptions[subject].replace("Sou", "É") + "?"
            )
            context["subject"] = subject
        search_results = zip(search_results, candidates_opinions)
        search_results = [{'opinion': opinion, 'candidate': candidate} for candidate, opinion in search_results]

        party_list = [candidate.party for candidate in CandidatePage.objects.all()]
        party_list = list(set(party_list))
        party_list.remove(None)

        paginator = Paginator(search_results, 20)
        page = request.GET.get('page', 1)
        try:
            candidates_list = paginator.page(page)
        except EmptyPage:
            candidates_list = paginator.page(paginator.num_pages)

        context["candidates_list"] = candidates_list
        context["subjects"] = list(subject_dict.keys())
        context["uf_list"] = uf_list
        context["party_list"] = party_list

        return context

@receiver(
    post_save, sender=FormSubmission, dispatch_uid="form_submission_link_candidate"
)
def form_submission_link_candidate(sender, instance: FormSubmission, **kwargs):
    form = instance.get_data()
    role_column = "e-candidatoa-a-qual-vaga-no-pleito-de-2022"

    if role_column not in form:
        return  # not a SurveysPage form

    builder = SurveyCandidateFactory(instance.id, form, role_column)
    builder.create_candidate()


class CasaChoices(models.TextChoices):
    SENADO = "senado", "senado"
    CAMARA = "camara", "camara"


class Proposicao(models.Model):
    id_externo = models.IntegerField(blank=False, null=False, primary_key=True)
    sigla_tipo = models.CharField(blank=False, null=False, max_length=6)
    numero = models.IntegerField(blank=False, null=False)
    ano = models.IntegerField(blank=False, null=False)
    ementa = models.TextField(blank=True, null=True)
    sobre = models.CharField(blank=False, null=False, max_length=90)
    casa = models.CharField(
        blank=False,
        null=False,
        max_length=6,
        choices=CasaChoices.choices,
    )

    def __str__(self) -> str:
        # MPV 867/2018
        return f"{self.sigla_tipo} {self.numero}/{self.ano}"

    @staticmethod
    def proposicoes_senado():
        return Proposicao.objects.filter(casa=str(CasaChoices.SENADO))

    @staticmethod
    def proposicoes_camara():
        return Proposicao.objects.filter(casa=str(CasaChoices.CAMARA))


class VotacaoProsicao(models.Model):
    proposicao = models.ForeignKey(
        Proposicao,
        on_delete=models.CASCADE,
        related_name="votacoes",
    )
    id_votacao = models.CharField(
        primary_key=True,
        blank=False,
        null=False,
        max_length=30,
    )
    data = models.DateField()
    data_hora_registro = models.CharField(blank=False, null=False, max_length=30)


class VotacaoParlamentar(models.Model):
    TIPOS_VOTO = {
        "camara": {
            "sim": "Sim",
            "nao": "Não",
            "obstrucao": "Obstrução",
            "abstencao": "Abstenção",
            "artigo_17": "Artigo 17",
        },
        "senado": {
            "sim": "Sim",
            "nao": "Não",
            "p_nrv": "P-NRV",
            "ap": "AP",
            "lp": "LP",
            "mis": "MIS",
            "abstencao": "Abstenção",
            "presidente_art_51": "Presidente (art. 51 RISF)",
        },
    }

    class Meta:
        indexes = [
            models.Index(
                fields=["id_parlamentar", "votacao_proposicao"],
                name="votacao_prop_deputado_idx",
            ),
        ]
        unique_together = (("id_parlamentar", "votacao_proposicao"),)

    votacao_proposicao = models.ForeignKey(
        VotacaoProsicao,
        on_delete=models.CASCADE,
        related_name="votacoes_parlamentares",
    )
    tipo_voto = models.CharField(blank=False, null=False, max_length=26)
    data = models.DateField()
    data_registro_voto = models.CharField(blank=False, null=False, max_length=30)
    id_parlamentar = models.IntegerField(blank=False, null=False)
    casa = models.CharField(
        blank=False,
        null=False,
        max_length=7,
        choices=CasaChoices.choices,
    )
