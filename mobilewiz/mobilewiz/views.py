from django.views import View
from django.shortcuts import render_to_response
from django.template import RequestContext

class Home(View):
    def get(self, request):
        context = {}
        return render_to_response("index.html", context, RequestContext(request))