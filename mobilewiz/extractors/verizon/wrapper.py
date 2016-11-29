import sys, os, json, re
import lxml.html as lh
from urllib.request import urlopen

base_url = 'https://www.verizonwireless.com/smartphones/'


class VerizonPhone():
    brand = ''
    title = ''
    url = ''
    prices = []


def print_usage():
    print("Usage ..")


def should_process_file(file):
    if not file.endswith('_2.html'):
        return False
    return True


def get_JSON_from_response(response):
    script = response.xpath('//*[@id="serviceContentId"]/text()')[0]
    script = str(script).strip()
    script = script.split('\n')[0]
    parts = script.split('"metaDataInfo"')
    if not len(parts) == 2:
        return False
    json_str = '{"metaDataInfo"' + parts[1]
    json_str = json_str.strip(';')

    print(json_str)

    json_obj = json.loads(json_str)

    return json_obj


def main():
    if len(sys.argv) < 1:
        print_usage()
    data_dir = sys.argv[1]
    output_file = open('output/extractions_verizon.json', 'w')

    all_phones = []
    for subdir, dirs, files in os.walk(data_dir):
        for file in files:
            if not should_process_file(file):
                continue
            response = lh.parse(urlopen('file:/' + os.path.join(subdir, file)))
            json_obj = get_JSON_from_response(response)

            if not json_obj:
                continue

            phone = VerizonPhone()
            print(subdir[len(data_dir):])
            title = json_obj['metaDataInfo']['title']
            phone.title = title.split("|")[0]

            phone.url = base_url + subdir[len(data_dir):]

            phone.brand = json_obj['mboxInfo']['seoBrand']

            mems = dict()

            for device in json_obj['devices']['skus']:
                price = dict()
                cur_mem = device['capacity']
                price['fullPrice'] = device['devicePrice'][0]['fullRetailPrice']
                price['number_of_installments'] = 24
                price['downPayment'] = device['devicePrice'][0]['creditOptionVOList'][0]['creditDiscountDownpament']
                price['emi'] = device['devicePrice'][0]['creditOptionVOList'][0]['creditDiscountedAmount']

                if cur_mem not in mems:
                    mems[cur_mem] = price
            phone.prices = mems

            all_phones.append(phone)
    print(all_phones)
    output_file.write(json.dumps(all_phones, default=lambda o: o.__dict__))
    print("Done.")


if __name__ == "__main__":
    main()
