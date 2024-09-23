# Following along https://pandas.pydata.org/docs/user_guide/10min.html 
# And playing with the code a little myself

import numpy as np
import pandas as pd


# Copy df from object_creation file
dates = pd.date_range("20240101", periods=6)
df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))



# Use DataFrame.head() and DataFrame.tail() 
# to view the top and bottom rows of the frame respectively

print(df.head())
print(df.tail(3))



# Display the DataFrame.index 
# or DataFrame.columns
print()
print(df.index)

print()
print(df.columns)


# Return a NumPy representation of the underlying data with DataFrame.to_numpy() 
# without the index or column labels

print()
print(df.to_numpy())


# describe() shows a quick statistic summary of your data
print(df.describe())


# Transposing your data:
print()
print(df.T)


# DataFrame.sort_index() sorts by an axis:
print()
print(df.sort_index(axis=1, ascending=False)) # axis : {0 or 'index', 1 or 'columns'}, default 0

# DataFrame.sort_values() sorts by values:s
print()
print(df.sort_values(by="C"))