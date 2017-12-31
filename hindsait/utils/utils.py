import feature_engg
from utils import plot

def print_error(error):
    """
    prints error; function might be updated further
    :param error:
    :return:
    """
    if error == 'level':
        print('level not in county/state')

    return 0


def visualize(feature, data, feature_df, state='all'):

    plt_title = feature_df[feature_df.field == feature]['variable_name'].tolist()[0]
    plt_desc = ''
    for key, value in feature_df[feature_df.field == feature].to_dict().items():
        if key in ['year_of_data', 'date_on', 'characteristics']:
            plt_desc += key + ": " + str(list(value.values())[0]) + "\n"

    feature_values_dict = feature_engg.extract_feature_data(data=data, feature=feature, state=state)

    # plot map
    US_map = plot.USMaps(state_borders=True, county_borders=True, state_names=False)
    if state.lower() == 'all':
        US_map.colour_code_usa_country(data=feature_values_dict, title=plt_title, desc=plt_desc)
    else:
        US_map.colour_code_usa_state(data=feature_values_dict, state=state, title=plt_title, desc=plt_desc)