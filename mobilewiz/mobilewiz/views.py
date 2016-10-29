from django.views import View
from django.shortcuts import render_to_response
from django.template import RequestContext
from haystack.query import SearchQuerySet
from django.http import HttpResponse
import json, urllib


class Home(View):
    def get(self, request):
        context = {}
        return render_to_response("index.html", context, RequestContext(request))


class Search(View):
    def get(self, request):
        sqs = SearchQuerySet().filter(content_auto=request.GET.get('q', ''))

        baseURLForItem = "/item/"

        suggestions = []

        for result in sqs:
            suggestion = dict()
            suggestion['title'] = result.title
            suggestion['url'] = baseURLForItem + urllib.parse.quote(result.title)
            suggestions.append(suggestion)
            if len(suggestions) >= 10:
                break
        data = json.dumps(suggestions)

        return HttpResponse(data, content_type='application/json')
