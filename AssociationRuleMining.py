import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from itertools import permutations
from mlxtend.preprocessing import TransactionEncoder

sns.set(style="darkgrid", color_codes=True)
pd.set_option('display.max_columns', 75)

###Preprocessing
# read dataset
df = pd.read_csv('MLDataset.csv') 

print(df.head())

#replacing empty value with 0.
df.fillna(0,inplace=True)

print(df.head())
print(df.describe())

color = plt.cm.rainbow(np.linspace(0, 1, 40))
df['0'].value_counts().head(40).plot.bar(color = color, figsize=(13,5))
plt.title('frequency of most popular items', fontsize = 20)
plt.xticks(rotation = 90 )
plt.grid()
plt.show()

#for using aprori need to convert data in list format

transactions = []
for i in range(0,len(df)):
    transactions.append([str(df.values[i,j]) for j in range(0,10) if str(df.values[i,j])!='0'])
 
print('# of transactions:',len(transactions))    

# Extract unique items.
flattened = [item for transaction in transactions for item in transaction]
items = list(set(flattened))
#print('# of items:',len(items))
#print(list(items))

# Compute and print rules.
rules = list(permutations(items, 2))
print('# of rules:',len(rules))
print(rules[:5])

# Instantiate transaction encoder and identify unique items
encoder = TransactionEncoder().fit(transactions)

# One-hot encode transactions
onehot = encoder.transform(transactions)

# Convert one-hot encoded data to DataFrame
onehot = pd.DataFrame(onehot, columns = encoder.columns_)

print(len(onehot))

# Compute the support
support = onehot.mean()
support = pd.DataFrame(support, columns=['support']).sort_values('support',ascending=False)


frequent_itemsets = apriori(onehot,min_support = 0.0040,max_len = 10, use_colnames = True)
print(len(frequent_itemsets))
frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))

# Compute all association rules using confidence
rules = association_rules(frequent_itemsets, metric = "confidence", min_threshold = 0.1)
rules.info()

# Compute all association rules for frequent_itemsets
rules = association_rules(frequent_itemsets, metric = "lift", min_threshold = 0.99)
rules.info()

#Visuliazition

#Heatmap
# Convert antecedents and consequents into strings
rules['antecedents'] = rules['antecedents'].apply(lambda a: ','.join(list(a)))
rules['consequents'] = rules['consequents'].apply(lambda a: ','.join(list(a)))

# Transform antecedent, consequent, and support columns into matrix
support_table = rules.pivot(index='consequents', columns='antecedents', values='confidence')

plt.figure(figsize=(10,6))
sns.heatmap(support_table, annot=True, cbar=False)
b, t = plt.ylim() 
b += 0.5 
t -= 0.5 
plt.ylim(b, t) 
plt.yticks(rotation=0)
plt.show() 

#ScatterPlot
# Generate association rules without performing additional pruning
rules = association_rules(frequent_itemsets, metric='support', 
                          min_threshold = 0.0)

# Generate scatterplot using support and confidence
plt.figure(figsize=(10,6))
sns.scatterplot(x = "support", y = "confidence", 
                size = "lift", data = rules)
plt.margins(0.01,0.01)
plt.show()
