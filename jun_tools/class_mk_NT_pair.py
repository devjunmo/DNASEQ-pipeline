import pandas as pd


class Mk_NT_pair():

    def __init__(self, pair_csv, ):

        pair_df = pd.read_csv(pair_info)
        pair_df.set_index('Tumor', inplace=True)

        pair_dict = pair_df.to_dict('index') # {tumor : {normal:_ grade:_} dict 형태. fname