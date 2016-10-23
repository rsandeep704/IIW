from django.views import View
from django.shortcuts import render_to_response
from django.template import RequestContext
from haystack.query import SearchQuerySet
from django.http import HttpResponse
import json


class Home(View):
    def get(self, request):
        context = {}
        return render_to_response("index.html", context, RequestContext(request))


class Search(View):
    def get(self, request):
        sqs = SearchQuerySet().filter(content_auto=request.GET.get('q', ''))
        suggestions = [result.title for result in sqs]

        # Make sure you return a JSON object, not a bare list.
        # Otherwise, you could be vulnerable to an XSS attack.
        the_data = json.dumps({
            'results': suggestions
        })
        return HttpResponse(the_data, content_type='application/json')
