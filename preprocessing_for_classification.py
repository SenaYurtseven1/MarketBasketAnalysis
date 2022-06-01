import csv
from itertools import groupby
import re


def canonicalize_dict(x):
    "Return a (key, value) list sorted by the hash of the key"
    return sorted(x.items(), key=lambda x: hash(x[0]))


def unique_and_count(lst):
    "Return a list of unique dicts with a 'count' key added"
    grouper = groupby(sorted(map(canonicalize_dict, lst)))
    return [dict(k + [("count", len(list(g)))]) for k, g in grouper]


def replace_str_index(text, index=0, replacement=''):
    return '%s%s%s' % (text[:index], replacement, text[index + 1:])


with open('Groceries data.csv', mode='r') as infile:
    line_nr = 0
    headers = []
    data = []
    arrivalCount = []
    newData = []
    allItems = []
    for line in csv.reader(infile):
        dictionary = {}
        membersArrival = {}
        if line_nr == 0:
            for header in line:
                headers.append(header)
            line_nr += 1
            continue
        dictionary[headers[0]] = line[0]
        dictionary[headers[1]] = line[1]
        dictionary[headers[2]] = line[2]
        membersArrival[line[0]] = line[1]
        arrivalCount.append(membersArrival)
        data.append(dictionary)
        if not line[2] in allItems:
            allItems.append(line[2])

# Gathering customers items together
customersAndBuyings = {}
for x in data:
    if x['Member_number'] in customersAndBuyings:
        if x['itemDescription'] not in customersAndBuyings[x['Member_number']]:
            customersAndBuyings[x['Member_number']] += ',' + x['itemDescription']
    else:
        customersAndBuyings[x['Member_number']] = x['itemDescription']

# calculate the visit counts of customers
regularsVisits = unique_and_count(arrivalCount)
regularVisitCounts = {}
for x in regularsVisits:
    for k in x.keys():
        if (not k == 'count') and (k in regularVisitCounts):
            regularVisitCounts[k] += 1
        elif not k == 'count':
            regularVisitCounts[k] = 1

# Calculate whether the customer is regular or not
regularCustomers = []
for k, v in regularVisitCounts.items():
    if v >= 4:
        regularCustomers.append(k)

# fill the blank spaces with commas
for k, v in customersAndBuyings.items():
    items = len(v.split(','))
    if not items == 26:
        commaString = ',' * (26 - items)
        customersAndBuyings[k] += commaString

# set the class attribute (regular, non-regular)
for k in customersAndBuyings.keys():
    for k2, v2 in regularVisitCounts.items():
        if k == k2:
            if v2 >= 4:
                customersAndBuyings[k] += ',' + 'regular'
            else:
                customersAndBuyings[k] += ',' + 'non-regular'

# Regular customer calculation
regularCount = 0
totalCustomers = len(regularVisitCounts)
for k, v in regularVisitCounts.items():
    if v >= 4:
        regularCount += 1
rate = regularCount / totalCustomers * 100

table = []
for x in range(totalCustomers):
    table.append('0' * len(allItems))

j = 0
for item in allItems:
    i = 0
    for k, v in customersAndBuyings.items():
        if item in v:
            table[i] = replace_str_index(table[i], j, '1')
        i += 1
    j += 1

i = 0

# add comma after 0 and 1's
for x in table:
    table[i] = ','.join(x[i:i + 1] for i in range(0, len(x), 1))
    i += 1

customers_list = list(regularVisitCounts)
c_index = 0
for k in customersAndBuyings.keys():
    for k2, v2 in regularVisitCounts.items():
        if k == k2:
            if v2 >= 4:
                table[c_index] += ',regular'
            else:
                table[c_index] += ',non-regular'
    c_index += 1

print(table)

print(
    'Müşteri sayısı = {} \n Devamlı Sayısı = {}, Devamlı müşteri oranı = {}'.format(totalCustomers, regularCount, rate))

# s = 'customerNo,item1,item2,item3,item4,item5,item6,item7,item8,item9,item10,item11,item12,item13,item14,item15,' \
#     'item16,item17,item18,item19,item20,item21,item22,item23,item24,item25,item26,class\n'

# for k, v in customersAndBuyings.items():
#     s += k + ',' + v + '\n'

with open('out.txt', mode='w') as out:
    out.write('customerNo,')
    for x in allItems:
        out.write(x + ',')
    out.write('class')
    out.write('\n')
    custIndex = 0
    for x in table:
        out.write(customers_list[custIndex] + ',')
        out.write(x + '\n')
        custIndex += 1


# maxItem = 0
# for k, v in customersAndBuyings.items():
#     items = len(v.split(','))
#     if items > maxItem:
#         maxItem = items
#
# print(maxItem)

# for x in arrivalCount:
#     for y in arrivalCount:
#         if x == y:
#             for key in x.keys():
#                 if key in regulars:
#                     regulars[key] += 1
#                 else:
#                     regulars[key] = 1
#
# print(regulars)


# sortedData = sorted(data, key=lambda i: i['Member_number'])
# print(sortedData)
# for x in range(sortedData):
#     if sortedData[x]['Member_number'] == sortedData[x+1]['Member_number']:


# for x in range(len(data)):
#     dictionary = {}
#     for y in range(x+1, len(data)):
#         if data[x]['Member_number'] == data[y]['Member_number']:
#             if data[x]['Member_number'] in dictionary:
#                 dictionary[data[x]['Member_number']] += "," + data[y]['itemDescription']
#             else:
#                 dictionary[data[x]['Member_number']] = data[x]['itemDescription'] + "," + data[y]['itemDescription']
#     if not dictionary == {}:
#         newData.append(dictionary)
#
# print(newData)
