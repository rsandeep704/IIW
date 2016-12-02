__author__ = 'sandeep'

import datetime

from haystack import indexes
from mobilewiz.models import GlobalMobilePhoneModel


class PhoneModel(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    modelName = indexes.CharField(model_attr='modelName')

    def get_model(self):
        return GlobalMobilePhoneModel

    def index_queryset(self, using = None):
        return self.get_model.objects.filter("")
