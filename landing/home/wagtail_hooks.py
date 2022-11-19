import re, json
from django.contrib import messages
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _
from wagtail.core.hooks import register
from wagtailstreamforms.serializers import FormSubmissionSerializer
from wagtailstreamforms.models import FormSubmissionFile

from wagtailstreamforms.utils.requests import get_form_instance_from_request

@register("before_serve_page")
def process_form(page, request, *args, **kwargs):
    if request.method != "POST":
        return
    form_def = get_form_instance_from_request(request)

    if not form_def:
        return

    form = form_def.get_form(
        request.POST, request.FILES, page=page, user=request.user
    )

    context = page.get_context(request)

    # CPF Validation
    cpf_valid = False
    cpf_field = list(filter(lambda x: x.label.lower() == "cpf", form))
    if len(cpf_field):
        cpf_field = cpf_field[0]
        cpf_value = cpf_field.value()
        cpf_value = cpf_value.replace('-','')
        cpf_value = cpf_value.replace('.','')
        cpf_valid = (
            cpf_value.isdigit()
            and len(cpf_value) == 11
        )
    else:
        cpf_valid = True

    # CNPJ Validation
    cnpj_valid = False
    cnpj_field = list(filter(lambda x: x.label.lower() == "cnpj", form))
    if len(cnpj_field):
        cnpj_field = cnpj_field[0]
        cnpj_value = cnpj_field.value()
        cnpj_value = cnpj_value.replace('.','')
        cnpj_value = cnpj_value.replace('/','')
        cnpj_value = cnpj_value.replace('-','')
        cnpj_valid = (
            cnpj_value.isdigit()
            and len(cnpj_value) == 14
        )
    else:
        cnpj_valid = True

    # Email Validation
    email_valid = False
    email_field = list(filter(lambda x: x.label.lower() == "e-mail da empresa", form))
    email_confirmation_field = list(
        filter(lambda x: x.label.lower() == "confirmação de e-mail", form)
    )
    email_regex = re.compile(
        r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    )
    if len(email_field) and len(email_confirmation_field):
        email_field = email_field[0]
        email_confirmation_field = email_confirmation_field[0]
        email_valid = (
            email_field.value() == email_confirmation_field.value()
            and re.fullmatch(email_regex, email_field.value())
        )
    else:
        email_valid = True

    if form.is_valid() and cpf_valid and email_valid and cnpj_valid:
        form_def.process_form_submission(form)

        if form_def.success_message:
            messages.success(
                request, form_def.success_message, fail_silently=True
            )

        redirect_page = form_def.post_redirect_page or page

        return redirect(redirect_page.get_url(request), context=context)

    else:
        context.update(
            {
                "invalid_stream_form_reference": form.data.get(
                    "form_reference"
                ),
                "invalid_stream_form": form,
            }
        )

        if not cpf_valid:
            messages.error(request, _("CPF inválido"), fail_silently=True)

        if not email_valid:
            messages.error(
                request,
                _("E-mail e confirmação de e-mail inválidos"),
                fail_silently=True,
            )

        if not cnpj_valid:
            messages.error(
                request, _("CNPJ inválido"), fail_silently=True
            )

        if form_def.error_message:
            messages.error(request, form_def.error_message, fail_silently=True)

        return TemplateResponse(
            request, page.get_template(request, *args, **kwargs), context
        )