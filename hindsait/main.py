from utils import download
from utils import read
from utils import plot
import pandas as pd
import os
import feature_engg


dir_list = ['./csv_data/', './vincent_map_data/', './basemaps/']

# download.download_data()
# download.create_dirs(dir_list)
# download.download_us_shape_files(resolution='low')

# read.read_sas_doc(path_in='./DOC/ahrf2016-17.sas', path_out='./csv_data/sas_doc.csv', write_df=True)
# read.read_data_wrt_sas_docs(path_in='./DATA/ahrf2017.asc', path_out='./csv_data/data.csv', write_df=True)
# read.read_excel_doc(path_in='./DOC/AHRF 2016-2017 Technical Documentation.xlsx', path_out='./csv_data/excel_doc.csv',
#                     write_df=True)
# read.read_fips_state_codes(path_in='./DATA/state.txt', path_out='./csv_data/fips_state_codes.csv', write_df=True)
# read.read_fips_all_codes(path_in='./DATA/all-geocodes-v2016.xlsx', path_out='./csv_data/fips_all_codes.csv',
#                          write_df=True)

# # read csv data
data = pd.read_csv('./csv_data/data.csv', low_memory=False, dtype=str)
excel_doc_df = pd.read_csv('./csv_data/excel_doc.csv', low_memory=False, dtype=str)
fips_all_codes_df = pd.read_csv('./csv_data/fips_all_codes.csv', low_memory=False, dtype=str)
fips_state_codes_df = pd.read_csv('./csv_data/fips_state_codes.csv', low_memory=False, dtype=str)

# feature eng/plot sample: 'county'
feature_df = feature_engg.get_features(data=data, doc_df=excel_doc_df, count_unique_feature_values=2)
feature = 'f1248115'
plt_title = feature_df[feature_df.field == feature]['variable_name'].tolist()[0]
plt_desc = ''
for key, value in feature_df[feature_df.field == feature].to_dict().items():
    if key in ['year_of_data', 'date_on', 'characteristics']:
        plt_desc += key+": "+str(list(value.values())[0])+"\n"

feature_values_dict = feature_engg.extract_feature_data(data=data, feature=feature, level='county')
# plot.colour_code(data=feature_values_dict, title=plt_title, desc=plt_desc, state_borders=True,
#                  county_borders=False, state_names=False)
plot.colour_code_usa_state(data=feature_values_dict, title=plt_title, desc=plt_desc, state_name='Alabama')


# feature eng/plot sample: 'state'
# feature_df = feature_engg.get_features(data=data, doc_df=excel_doc_df, count_unique_feature_values=2)
# feature = 'f1248115'
# plt_title = feature_df[feature_df.field == feature]['variable_name'].tolist()[0]
# plt_desc = ''
# for key, value in feature_df[feature_df.field == feature].to_dict().items():
#     if key in ['year_of_data', 'date_on', 'characteristics']:
#         plt_desc += key+": "+str(list(value.values())[0])+"\n"
#
# feature_values_dict = feature_engg.extract_county_level_feature_data(data=data, feature=feature)
# plot.colour_code(data=feature_values_dict, title=plt_title, desc=plt_desc, state_borders=True, county_borders=False,
#                  state_names=False, level='state')



