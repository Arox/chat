from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class WindowView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        kwargs['host'] = self.request.META['HTTP_HOST']
        return super().get_context_data(**kwargs)
