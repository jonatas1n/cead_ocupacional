from django import template
from home.models import LandingPage

register = template.Library()

@register.inclusion_tag("home/footer.html", takes_context=True)
def footer(context):
    request = context.get("request")
    home_page = LandingPage.objects.all()[0]
    social_media = home_page.social_media
    return {
        "request": request,
        "social_media": social_media
    }
