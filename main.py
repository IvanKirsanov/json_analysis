import json
import codecs
import re
import csv

my_file = codecs.open("msk.json", "r", "utf_8_sig")

res = my_file.read()
res = json.loads(res)
admins = ['Иван Кирсанов', ...]

result_list = []

for usr in res['messages']:
    try:
        if usr['from'] in admins and '?' in str(usr['text']):
            try:
                result_list.append(
                    {"message_id": usr['id'], "number_order": re.search(r'\d[\d ]{9}', str(usr['text'])).group(),
                     "time_soglos": usr['date']})
            except AttributeError:
                continue
            except TypeError:
                continue
    except KeyError:
        continue

# согласования с реплаем
for usr in res['messages']:
    try:
        if usr['from'] not in admins:
            for el in result_list:
                if el.get('message_id') == usr['reply_to_message_id']:
                    el["who_replied"] = usr['from']
                    el["time_replied"] = usr['date']
    except KeyError:
        continue

check = 0
pos = 0

# согласования без реплая
for usr in res['messages']:
    if check == 0:
        for el in result_list:
            if el.get('who_replied') is None and el.get('message_id') == usr['id']:
                check = 1
                pos = el.get('message_id')
                break
    else:
        check = 0
        if usr['from'] not in admins:
            for el in result_list:
                if el.get('message_id') == pos:
                    el["who_replied"] = usr['from']
                    el["time_replied"] = usr['date']
        pos = 0

for usr in res['messages']:
    if '#' in str(usr['text']):
        for el in result_list:
            if el['message_id'] == usr['id']:
                position = str(usr['text']).find('#')+1
                el['tag'] = str(usr['text'])[position:position+5].lower()

for el in result_list:
    if el.get('who_replied') is None:
        el["who_replied"] = '-'
        el["time_replied"] = '-'
    if el.get('tag') is None:
        el['tag'] = '-'

with open('msk.csv', 'w', newline='') as f:
    writer = csv.DictWriter(
        f, fieldnames=list(result_list[0].keys()), delimiter=';')
    writer.writeheader()
    for d in result_list:
        writer.writerow(d)
