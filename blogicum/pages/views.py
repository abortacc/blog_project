from django.views.generic import TemplateView


class AboutTemplateView(TemplateView):
    template = 'pages/about.html'


class RulesTemplateView(TemplateView):
    template = 'pages/rules.html'
