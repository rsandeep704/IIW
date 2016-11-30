__author__ = 'sandeep'

from django.contrib import admin
from mobilewiz.models import GlobalMobilePhoneModel, GlobalMobilePhones, GlobalSpecs, ATTData, VerizonData, TMobileData

admin.site.register(GlobalMobilePhoneModel)
admin.site.register(GlobalMobilePhones)
admin.site.register(GlobalSpecs)

admin.site.register(ATTData)
admin.site.register(VerizonData)
admin.site.register(TMobileData)
