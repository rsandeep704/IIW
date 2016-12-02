from django.views import View
from django.shortcuts import render_to_response
from django.template import RequestContext
from haystack.query import SearchQuerySet
from django.http import HttpResponse
from mobilewiz.fonoAPI import FonApi
from mobilewiz.models import GlobalMobilePhones, GlobalMobilePhoneModel
import json, urllib, re


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
            suggestion['modelName'] = result.modelName
            suggestion['id'] = str(result.id)
            suggestion['url'] = baseURLForItem + urllib.parse.quote(result.modelName)
            suggestions.append(suggestion)
            if len(suggestions) >= 10:
                break
        data = json.dumps(suggestions)

        return HttpResponse(data, content_type='application/json')


class Item(View):
    def get(self, request, modelName):
        #sqs = SearchQuerySet().filter(content_auto=modelName)
        phonesData = GlobalMobilePhones.objects.filter(phone_model=GlobalMobilePhoneModel.objects.filter(modelName=modelName).get()).order_by('totalCost')
        suggestions = []
        fon = FonApi('4986e17810f1f9779514d993c6e835f67934d9c26126d42b')
        phones = fon.getdevice(modelName)
        phoneDescription = {}

        try:
            for phone in phones:
                # print(phone)
                if str(re.sub(phone['Brand'], "", phone['DeviceName'], flags=re.IGNORECASE)).lstrip(" ") == modelName:
                    phoneDescription = phone
                    break

        except:
            phoneDescription = {}
        for result in phonesData:
            suggestion = dict()
            suggestion['modelName'] = str(result.phone_model)
            suggestion['title'] = result.title
            suggestion['emi'] = str(result.emi)
            suggestion['down_payment'] = str(result.down_payment)
            suggestion['total_cost'] = str(result.totalCost)
            suggestion['no_of_installments'] = result.no_of_installments
            suggestion['url'] = str(result.url)
            suggestion['company'] = result.company
            suggestion['imageURL'] = str(result.imageUrl)
            suggestion['companyImage'] = str(result.company).lower()
            suggestions.append(suggestion)
            #print(suggestion)
            if len(suggestions) >= 10:
                break
        data = suggestions
        return render_to_response("item.html", {'data': data, 'description': phoneDescription}, RequestContext(request))