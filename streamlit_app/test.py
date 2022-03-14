import pickle

dictt = pickle.load(open("./example_debate_1_processed.pkl",'rb'))
print(dictt[2])

print(pickle.format_version)

import pandas as pd
print(pd.__version__)