import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from apyori import apriori
from itertools import permutations

###Preprocessing
# read dataset
df = pd.read_csv('MLDataset.csv') 

#replacing empty value with 0.
df.fillna(0,inplace=True)

"""
color = plt.cm.rainbow(np.linspace(0, 1, 40))
df['Stok Adı'].value_counts().head(40).plot.bar(color = color, figsize=(13,5))
plt.title('frequency of most popular items', fontsize = 20)
plt.xticks(rotation = 90 )
plt.grid()
plt.show()
"""

df=df.drop("Borç Tutarı",axis=1)
df=df.drop("Alacak Tutarı",axis=1)
df=df.drop("Borç Bakiyesi",axis=1)
df=df.drop("Alacak Bakiyesi",axis=1)
df=df.drop("Adres",axis=1)
df=df.drop("Adı",axis=1)
"""
#for using aprori need to convert data in list format

transactions = []
for i in range(0,len(df)):
    transactions.append([str(df.values[i,j]) for j in range(0,10) if str(df.values[i,j])!='0'])
 
# Extract unique items.
flattened = [item for transaction in transactions for item in transaction]
items = list(set(flattened))
#print('# of items:',len(items))
#print(list(items))


# Compute and print rules.
rules = list(permutations(items, 2))
#print('# of rules:',len(rules))
#print(rules[-1:])


#Call apriori function which requires minimum support, confidance and lift, min length is combination of item default is 2".    
rules = apriori(transactions,min_support=0.01,min_confidence=0.01,min_lift=1)

# Visualizing the list of rules
results = list(rules)
for i in results:
    print('\n')
    print(i)
    print('**********') """