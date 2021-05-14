import os
import csv
import re
import difflib
import json
import csv
from datetime import datetime, date, time, timedelta
months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

def read_json(filename):
    return json.loads(open(filename).read())
def write_csv(data,filename):
    qwe = 0
    with open(filename, 'w+') as outf:
      for i in range(len(data)):
          if(data[i]['link'].find('html') != -1):
            writer = csv.DictWriter(outf, data[i].keys())
            qwe = 1
            break
      if(qwe == 0):
        return
      writer.writeheader()
      for row in data:
        if(row['link'].find('html') != -1):
          writer.writerow(row)
write_csv(read_json('Lots.json'), 'Input.csv')

with open('Input.csv') as f:
  reader = csv.DictReader(f)
  lots = list(reader)
for lot in lots: 
  del lot['prov']
  del lot['Auction_name']
  lot['Author'] = lot['True_Author'].lower()
  del lot['True_Author']
  foo = ''
  for part in lot['Estimate_from'].split(','):
    foo = foo + part
  if(foo == ' '):
    foo = '0'
  lot['Estimate_from'] = int(foo)
  foo = ''
  for part in lot['Estimate_to'].split(','):
    foo = foo + part
  if(foo == ' '):
    foo = '0'
  lot['Estimate_to'] = int(foo)
  foo = lot['Price'].lower().expandtabs().split('\n')
  if(foo[0] == '0'):
    lot['Price'] = '0'
  else:
    lot['Price'] = foo[2][56:-3]
  foo = ''
  for part in lot['Price'].split(','):
    foo = foo + part
  if(foo == ' '):
    foo = '0'
  lot['Price'] = int(foo)
  date = lot['Auction_date'][2:-2].split('\', \'')
  info = [date[12], date[13], date[14]]
  month = ''
  if(info[1] == 'January'):
    month = '01'
  if(info[1] == 'February'):
    month = '02'
  if(info[1] == 'March'):
    month = '03'
  if(info[1] == 'April'):
    month = '04'
  if(info[1] == 'May'):
    month = '05'
  if(info[1] == 'June'):
    month = '06'
  if(info[1] == 'July'):
    month = '07'
  if(info[1] == 'August'):
    month = '08'
  if(info[1] == 'September'):
    month = '09'
  if(info[1] == 'October'):
    month = '10'
  if(info[1] == 'November'):
    month = '11'
  if(info[1] == 'December'):
    month = '12'
  lot['Auction_date'] = info[0]+'.'+month+'.'+info[2]
  time = lot['Auction_time'].expandtabs()
  if(lot['Currency'] == ''):
    lot['Currency'] = 'USD'
  lot['Norm_price'] = int(lot['Price'] * (1+infl[(2020-int(info[2]))*12 + int(month)-1]/100) * conveyor(1, lot['Currency'], 'USD'))
  lot['Norm_estimate_from'] = int(lot['Estimate_from'] * (1+infl[(2020-int(info[2]))*12 + int(month)-1]/100) * conveyor(1, lot['Currency'], 'USD'))
  lot['Norm_estimate_to'] = int(lot['Estimate_to'] * (1+infl[(2020-int(info[2]))*12 + int(month)-1]/100) * conveyor(1, lot['Currency'], 'USD'))
  while "  " in time:
    time = time.replace("  ", " ")
  if(time == ''):
    time = '  00:00 AM GMT'
  time = time[2:]
  info = time.split(' ')
  time = datetime.strptime(lot['Auction_date'] + ' ' +info[0], "%d.%m.%Y %H:%M")
  d = lot['Description'].lower()
  while "  " in d:
    d = d.replace("  ", " ")
  info = d.split('provenance')
  if(len(info) > 1):
    lot['Provenance'] = info[1].split('literature')[0].split('exhibited')[0]
  else:
    lot['Provenance'] = ''
  lot['Description'] = info[0].split('read condition report')[0].replace('\n', '').replace('\t', '')
i = 0
j = 0
pairs = []
while i < len(lots):
      if(lots[i]['Price'] == 0 or lots[i+1]['Price'] == 0):
        i = i + 2
        continue
      if(len(lots[i]['Author']) < len(lots[i+1]['Author']) and lots[i]['Author'] != '#'):
        lots[i+1]['Author'] = lots[i]['Author']
      else:
        lots[i]['Author'] = lots[i+1]['Author']
      if(len(lots[i]['Art']) < len(lots[i+1]['Art']) and lots[i]['Art'] != '#'):
        lots[i+1]['Art'] = lots[i]['Art']
      else:
        lots[i]['Art'] = lots[i+1]['Art']
      if(lots[i]['Art'] == '#' or lots[i]['Art'] == '#'):
        i += 2
        continue
      flag = 0
      for s in lots[i+1]['Provenance'].split('\n'):
        if('ot ' + str(lots[i]['Lot_number']) in s and lots[i]['Auction_date'].split('.')[2] in s and ' ' + str(int(lots[i]['Auction_date'].split('.')[0])) in s and months[int(lots[i]['Auction_date'].split('.')[1])-1] in s):
          flag = 1
        flag = 0
        i += 2
        continue
      if('bronze' in lots[i]['Description'] or 'bronze' in lots[i+1]['Description'] or 'metal' in lots[i]['Description'] or 'metal' in lots[i+1]['Description'] or 'silver' in lots[i]['Description'] or 'silver' in lots[i+1]['Description']):
        i += 2
        continue
      lots[i]['Provenance'] = lots[i]['Provenance']
      lots[i+1]['Provenance'] = lots[i+1]['Provenance']
      pairs.append({})
      for index in ('Lot_number',	'Estimate_from',	'Estimate_to',	'Currency',	'Price',	'Auction_date',	'Auction_time',	'Auction_location',	'Description',	'link', 'Provenance', 'Norm_price', 'Norm_estimate_from', 'Norm_estimate_to'):
        pairs[j][index+'1'] = lots[i][index]
        pairs[j][index+'2'] = lots[i+1][index] 
      pairs[j]['Author'] = lots[i]['Author']
      pairs[j]['Art'] = lots[i]['Art']
      pairs[j]['Image'] = lots[i+1]['Image']
      pairs[j]['Days_distance'] =abs(datetime.strptime(lots[i]['Auction_date'], "%d.%m.%Y") - datetime.strptime(lots[i+1]['Auction_date'], "%d.%m.%Y")).days
      pairs[j]['Resale_income'] = lots[i+1]['Norm_price'] - lots[i]['Norm_price']
      pairs[j]['Estimate_from_income'] = lots[i+1]['Norm_estimate_from'] - lots[i]['Norm_estimate_from']
      pairs[j]['Estimate_to_income'] = lots[i+1]['Norm_estimate_to'] - lots[i]['Norm_estimate_to']
      flag = 0
      for qwe in range(j):
        if((pairs[qwe]['link1'] == pairs[j]['link1'] and pairs[qwe]['link2'] == pairs[j]['link2'])):
          del pairs[j]
          flag = 1
          break
      if flag == 1:
        i += 2
        continue
      if(pairs[j]['link1'] == pairs[j]['link2']):
        del pairs[j]
        i += 2
        continue
      i += 2
      j += 1
with open('AFilling.csv', 'w') as csvfile:
    fieldnames = ['Author',	'Art',	'Lot_number',	'Estimate_from',	'Estimate_to',	'Currency',	'Price',	'Image',	'Auction_date',	'Auction_time',	'Auction_location',	'Description',	'link', 'Provenance', 'Norm_price', 'Norm_estimate_from', 'Norm_estimate_to']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter = '\t')
    writer.writeheader()
    i = 0
    j = 0
    while i < len(lots):
      if(len(lots[i]['Author']) < len(lots[i+1]['Author']) and lots[i]['Author'] != '#'):
        lots[i+1]['Author'] = lots[i]['Author']
      else:
        lots[i]['Author'] = lots[i+1]['Author']
      if(len(lots[i]['Art']) < len(lots[i+1]['Art']) and lots[i]['Art'] != '#'):
        lots[i+1]['Art'] = lots[i]['Art']
      else:
        lots[i]['Art'] = lots[i+1]['Art']
      if(lots[i]['Art'] == '#' or lots[i]['Art'] == '#'):
        i += 2
        continue  
      if(len(lots[i]['Author']) < len(lots[i+1]['Author']) and lots[i]['Author'] != '#'):
        lots[i+1]['Author'] = lots[i]['Author']
      else:
        lots[i]['Author'] = lots[i+1]['Author']
      if(len(lots[i]['Art']) < len(lots[i+1]['Art']) and lots[i]['Art'] != '#'):
        lots[i+1]['Art'] = lots[i]['Art']
      else:
        lots[i]['Art'] = lots[i+1]['Art']
      if(lots[i]['Art'] == '#' or lots[i]['Art'] == '#'):
        i += 2
        continue
      if('bronze' in lots[i]['Description'] or 'bronze' in lots[i+1]['Description'] or 'metal' in lots[i]['Description'] or 'metal' in lots[i+1]['Description'] or 'silver' in lots[i]['Description'] or 'silver' in lots[i+1]['Description'] or 'steel' in lots[i]['Description'] or 'steel' in lots[i+1]['Description']):
        i += 2
        continue
      writer.writerow(lots[i])
      writer.writerow(lots[i+1])
      i += 2
      j += 2
with open('Resale.csv', 'w') as csvfile:
    fieldnames = ['Lot_number1', 'Lot_number2', 'Estimate_from1', 'Estimate_from2', 'Estimate_to1', 'Estimate_to2', 'Currency1', 'Currency2', 'Price1', 'Price2', 'Auction_date1', 'Auction_date2', 'Auction_time1', 'Auction_time2', 'Auction_location1', 'Auction_location2', 'Description1', 'Description2', 'link1', 'link2', 'Provenance1', 'Provenance2', 'Norm_price1', 'Norm_price2', 'Norm_estimate_from1', 'Norm_estimate_from2', 'Norm_estimate_to1', 'Norm_estimate_to2', 'Author', 'Art', 'Image', 'Days_distance', 'Resale_income', 'Estimate_from_income', 'Estimate_to_income']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter = '\t')
    writer.writeheader()
    for i in range(len(pairs)):
      writer.writerow(pairs[i])
