from django.views.generic import TemplateView
import os
import requests
import json

api_url = 'http://_api.internal:4280/v1/apps/[REDACTED]/machines'
api_token = f"Bearer {os.getenv('FLY_API_TOKEN')}"
api_request = requests.get(api_url, headers={"Authorization": api_token}).text
machine_info = json.loads(api_request)[0]

class HomepageView(TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['machines'] = machine_info
        return context