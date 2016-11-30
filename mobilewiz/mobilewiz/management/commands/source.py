from django.core.management.base import BaseCommand, CommandError
import json
from mobilewiz.models import ATTData, VerizonData, TMobileData


def source_att():
    with open('data/extractions_att.json') as json_data_file:
        json_data = json.load(json_data_file)
        json_data_file.close()
    ATTData.objects.all().delete()

    for json_obj in json_data:
        att_phone = ATTData()
        att_phone.memory = json_obj['memory']
        att_phone.brand = json_obj['brand']
        att_phone.url = json_obj['url']
        att_phone.name = json_obj['title']
        att_phone.model = json_obj['model']
        att_phone.emi = json_obj['emi']
        att_phone.total_cost = json_obj['full_price']
        att_phone.no_of_installments = json_obj['number_of_installments']
        att_phone.down_payment = json_obj['prices - down_payment']
        att_phone.sku_id = json_obj['sku_id']

        att_phone.save()


def source_verizon():
    with open('data/extractions_verizon.json') as json_data_file:
        json_data = json.load(json_data_file)
        json_data_file.close()

    VerizonData.objects.all().delete()

    for json_obj in json_data:
        verizon_phone = VerizonData()
        verizon_phone.memory = json_obj['memory']
        verizon_phone.brand = json_obj['brand']
        verizon_phone.url = json_obj['url']
        verizon_phone.name = json_obj['name']
        verizon_phone.emi = json_obj['emi']
        verizon_phone.total_cost = json_obj['full_price']
        verizon_phone.no_of_installments = json_obj['no_of_months']
        verizon_phone.down_payment = json_obj['down_payment']

        verizon_phone.save()


def source_tmobile():
    with open('data/extractions_tmobile.json') as json_data_file:
        json_data = json.load(json_data_file)
        json_data_file.close()

    TMobileData.objects.all().delete()

    for json_obj in json_data:
        tmobile_phone = TMobileData()
        tmobile_phone.memory = json_obj['memory']
        tmobile_phone.brand = json_obj['brand']
        tmobile_phone.url = json_obj['url']
        tmobile_phone.name = json_obj['title']
        tmobile_phone.emi = json_obj['emi']
        tmobile_phone.total_cost = json_obj['full_price']
        tmobile_phone.no_of_installments = json_obj['number_of_months']
        tmobile_phone.down_payment = json_obj['down_payment']

        tmobile_phone.save()
    pass


class Command(BaseCommand):
    help = 'Build global databse from the local source'

    def handle(self, *args, **options):
        source_att()
        source_verizon()
        source_tmobile()
