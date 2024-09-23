# Following along https://pandas.pydata.org/docs/user_guide/10min.html 
# And playing with the code a little myself

import numpy as np
import pandas as pd


# Copy df from object_creation file
dates = pd.date_range("20240101", periods=6)
df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))



# For a DataFrame, passing a single label selects a columns 
# and yields a Series equivalent to df.A:
print(df["A"])


# For a DataFrame, passing a slice ':' selects matching rows:
print()
print(df.head)
print(df[0:3])


##### Selection by label

# Selecting a row matching a label
print()
print(df.loc[dates[0]])

# Selecting all rows (:) with a select column labels
print(df.loc[:, ["A", "B"]])

# For label slicing, both endpoints are included:
print()
print(df.loc["20240102":"20240104", ["A", "B"]])

# Selecting a single row and column label returns a scalar
print('single row & col: ', df.loc[dates[0], "A"])
df.at[dates[0], "A"] # faster access than ^