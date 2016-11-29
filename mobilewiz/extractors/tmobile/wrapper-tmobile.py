__author__ = 'Sandeep R'

import lxml.html as lh
import os, json
from urllib.request import urlopen
import requests
import sys

_baseURL = "http://www.t-mobile.com/cell-phones/"


class TMobilePhoneRaw():
    def __init__(self):
        self.URL = ''
        self.mems = dict()
        self.title = ''

    def __str__(self):
        return self.title + "\n" + str(self.mems)


class TMobilePhone():
    def __init__(self):
        self.URL = ''
        self.prices = dict()
        self.title = ''

    def __str__(self):
        return self.title + "\n" + str(self.prices)


def getDataFromWeb(id):
    url = 'http://www.t-mobile.com/Services/Activation/ActivationService.svc/deviceprice?DeviceID'
    headers = {
        'Host': 'www.t-mobile.com',
        'Origin': 'http://www.t-mobile.com',
        'Referer': 'http://www.t-mobile.com/cell-phones/apple-iphone-7-plus.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json'
    }
    data = {
        "DeviceID": id
    }
    r = requests.post(url, headers=headers, data=json.dumps(data))

    r = r.json()
    try:
        full_price = r['Device'][0]['FullPrice']
    except Exception as e:
        return 0, 0, 0, 0
    try:
        down_payment = r['Device'][0]['EIP']['DownPayment']
        emi = r['Device'][0]['EIP']['MonthlyPayment']
        number_of__installments = r['Device'][0]['EIP']['NumberOfInstallments']
    except Exception as e:
        return full_price, 0, 0, 0
    return full_price, down_payment, emi, number_of__installments


def getPrices(extracted_phones):
    phones = list()

    for extracted_phone in extracted_phones:
        phone = TMobilePhone()
        phone.title = extracted_phone.title
        phone.URL = extracted_phone.URL
        for memory in extracted_phone.mems.keys():
            for id in extracted_phone.mems[memory]:
                (full_price, downPayment, emi, no_of_installments) = getDataFromWeb(id)
                prices_dict = {
                    'full_price': full_price,
                    'downPayment': downPayment,
                    'emi': emi,
                    'no_of_installments': no_of_installments
                }
                if phone.prices.get(memory, True) or phone.prices['memory'].get(full_price, 99999) < full_price:
                    phone.prices[memory] = prices_dict
        phones.append(phone)
    return phones


def main():
    data_dir = sys.argv[1]
    outputFile = open('output/extractions_tmobile.json', 'w')
    extracted_phones = list()
    print("Extracting device IDs ..")
    for file in os.listdir(data_dir):
        if not file.endswith("_2.html") and file.endswith(".html"):

            response = lh.parse(urlopen('file:/' + data_dir + file)).getroot()
            phone = TMobilePhoneRaw()
            phone.URL = (_baseURL + file).strip('\n').strip()
            try:
                title = response.xpath(
                    '/html/body/div[5]/div[1]/div[1]/section/div[1]/div/div/div[4]/h1/text()')[0]
            except Exception as e:
                print("Skipping the file " + str(file))
                continue
            phone.title = title
            print('titles are ' + str(title))

            phoneids = response.xpath('//*[@id="specifications"]/div/div[3]/ul[4]/li/@data-id')
            memories = response.xpath('//*[@id="specifications"]/div/div[3]/ul[4]/li/node()')

            if (len(phoneids) != len(memories)):
                print("Skipping the file " + str(file))
                continue
            mems = {}
            print(memories)
            for i in range(0, len(memories)):
                memory = memories[i]
                if memory not in mems:
                    mems[memory] = list()
                mems[memory].append(phoneids[i])

            phone.mems = mems
            extracted_phones.append(phone)
    print("Extracting prices ..")
    fullTMobileData = getPrices(extracted_phones)

    outputFile.write(json.dumps(fullTMobileData, default=lambda o: o.__dict__))
    print("Done.")


if __name__ == '__main__':
    main()
