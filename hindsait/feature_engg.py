import pandas as pd
from utils.errors import print_error


def extract_feature_data(data, feature, state='all', level='county'):
    """
    extracts the features_values from the data. performs groupby on feature of our interest, makes a dictionary of each
    unique value in the feature and assings the countys or states as lists to relevant key in the dictionary.
    :param data: a pandas dataframe
    :param feature: feature of interest in the dataframe passed
    :param state: include only one state or all of them. In the case of one state pass state_name, abbrevation or fpcode
    :param level: in what detail do you want the information county level or state level
    :return: dictionary
    """
    state = state.lower()
    state_df = pd.read_csv('./csv_data/fips_state_codes.csv', dtype=str)

    if state != 'all':
        if state in state_df['STATE_NAME'].str.lower().tolist():
            key = 'f00008'
        elif state in state_df['STATE']:
            key = 'f00011'
        elif state in state_df['STUSAB'].str.lower().tolist():
            key = 'f12424'
        else:
            print('state not found')
        data = data[data[key].str.lower() == state]

    if level == 'county':
        feature_values_dict = data[['f00012', feature]].groupby(feature)['f00012'].apply(list).to_dict()
        return feature_values_dict
    elif level == 'state':
        feature_values_dict = data[['f00011', feature]].groupby(feature)['f00012'].apply(list).to_dict()
        return feature_values_dict
    else:
        print_error(error='level')


def get_features(data, doc_df,count_unique_feature_values):
    """
    counts the unique feature_values for each feature in the dataframe and return only the count value of interest with
    the features documentation.
    :param data: data frame
    :param doc_df: feature documentation
    :param count_unique_feature_values: nunique value of interest in each feature
    :return: dataframe
    """
    if count_unique_feature_values > 5:
        print('Current plot only supports 5 values for each feature: Add colours to support more')

    nunique_columns_df = pd.DataFrame(data.nunique()).reset_index()
    nunique_columns_df.columns = ['column', 'nunique']
    feature_list = nunique_columns_df[
        nunique_columns_df['nunique'] == count_unique_feature_values]['column'].tolist()
    feature_df = doc_df[doc_df.field.isin(feature_list)]
    # print(feature_df)
    return feature_df

