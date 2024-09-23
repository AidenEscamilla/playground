# Following along https://pandas.pydata.org/docs/user_guide/10min.html 
# And playing with the code a little myself

import numpy as np
import pandas as pd

# Creating a Series by passing a list of values, letting pandas create a default RangeIndex
s = pd.Series([1.389, 'test', 5, np.nan, 'd', 8])

print(s)



# Creating a DataFrame by...
# passing a NumPy array with a datetime index using date_range() and labeled columns:

dates = pd.date_range("20240101", periods=6)
print(dates)

df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))
print(df)



# passing a dictionary of objects where the keys are the column labels
# and the values are the column values

dict_df = pd.DataFrame(
    {
        "A": 1.0,
        "B": pd.Timestamp("20240102"),
        "C": pd.Series(1, index=list(range(4)), dtype="float32"),
        "D": np.array([3] * 4, dtype="int32"),
        "E": pd.Categorical(["test", "train", "test", "train"]),
        "F": "foo",
    }
)

print(dict_df)
print(dict_df.dtypes)
