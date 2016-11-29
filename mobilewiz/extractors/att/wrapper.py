from urllib.request import urlopen
import lxml.html as lh
import os, sys
import requests
import json

base_url = "https://www.att.com"


class ATTPhone():
    def __init__(self):
        self.URL = ''
        self.prices = dict()
        self.title = ''
        self.sku_id = ''
        self.model = ''

    def __str__(self):
        return self.title + "\n" + str(self.prices)


def getInitialIDs():
    initial_skus = set()
    response = lh.parse(urlopen('file:' + os.path.dirname(os.path.realpath(__file__)) + '/data/index.html')).getroot()
    grid_items = response.xpath("//div[starts-with(@id,'item_sku')]/@id")
    for grid_item in grid_items:
        split_items = grid_item.split('_')
        if len(split_items) == 2 and split_items[1].startswith('sku'):
            initial_skus.add(split_items[1])
    return initial_skus


def main():
    outputFile = open('output/extractions_att.json', 'w')
    print("Finding all phones")
    initial_skus = getInitialIDs()
    completed_skus = set()
    phones = list()
    models = set()

    print("Finding prices")
    for sku in initial_skus:
        url = 'https://www.att.com/services/shopwireless/model/att/ecom/api/DeviceDetailsActor/getDeviceProductDetails?includeAssociatedProducts=true&includePrices=true&skuId=' + sku
        r = requests.post(url)
        r = r.json()
        cur_skus = r['result']['methodReturnValue']['skuItems']

        for cur_sku in cur_skus:
            if cur_sku not in completed_skus:
                phone = ATTPhone()
                phone.title = r['result']['methodReturnValue']['skuItems'][cur_sku]['skuDisplayName']
                phone.model = r['result']['methodReturnValue']['skuItems'][cur_sku]['model']
                phone.URL = base_url + r['result']['methodReturnValue']['skuItems'][cur_sku]['devicePageURL']
                prices = dict()
                prices['full_price'] = r['result']['methodReturnValue']['skuItems'][cur_sku]['priceList'][0][
                    'itemPrice']
                if len(r['result']['methodReturnValue']['skuItems'][cur_sku]['priceList']) > 2:
                    prices['number_of_installments'] = \
                        r['result']['methodReturnValue']['skuItems'][cur_sku]['priceList'][2][
                            'leaseTotalMonths']
                    prices['emi'] = \
                        r['result']['methodReturnValue']['skuItems'][cur_sku]['priceList'][2]['monthlyLeasePrice']
                    prices['down_payment'] = r['result']['methodReturnValue']['skuItems'][cur_sku]['priceList'][2][
                        'dueToday']
                elif len(r['result']['methodReturnValue']['skuItems'][cur_sku]['priceList']) > 1:
                    prices['number_of_installments'] = \
                        r['result']['methodReturnValue']['skuItems'][cur_sku]['priceList'][1][
                            'leaseTotalMonths']
                    prices['emi'] = \
                        r['result']['methodReturnValue']['skuItems'][cur_sku]['priceList'][1]['monthlyLeasePrice']
                    prices['down_payment'] = r['result']['methodReturnValue']['skuItems'][cur_sku]['priceList'][1][
                        'dueToday']
                else:
                    prices['number_of_installments'] = '0'
                    prices['down_payment'] = 0
                    prices['emi'] = 0

                phone.prices = prices
                if phone.model not in models:
                    phones.append(phone)
                    models.add(phone.model)
                completed_skus.add(cur_sku)
    outputFile.write(json.dumps(phones, default=lambda o: o.__dict__))
    print("Done.")


if __name__ == '__main__':
    main()
