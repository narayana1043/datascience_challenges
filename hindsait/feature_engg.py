import pandas as pd
from utils.utils import print_error


def extract_feature_data(data, feature, level='county'):
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

    :param data:
    :param excel_doc_df:
    :param count_unique_feature_values:
    :return:
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

