from utils import download
from utils import read
from utils import plot
import pandas as pd
import feature_engg


dir_list = ['./csv_data/', './vincent_map_data/', './basemaps/']

# below code is not required once the files are downloaded
# ******************************************************** #
download.download_data()
download.create_dirs(dir_list)
download.download_us_shape_files(resolution='low')

read.read_sas_doc(path_in='./DOC/ahrf2016-17.sas', path_out='./csv_data/sas_doc.csv', write_df=True)
read.read_data_wrt_sas_docs(path_in='./DATA/ahrf2017.asc', path_out='./csv_data/data.csv', write_df=True)
read.read_excel_doc(path_in='./DOC/AHRF 2016-2017 Technical Documentation.xlsx', path_out='./csv_data/excel_doc.csv',
                    write_df=True)
read.read_fips_state_codes(path_in='./DATA/state.txt', path_out='./csv_data/fips_state_codes.csv', write_df=True)
read.read_fips_all_codes(path_in='./DATA/all-geocodes-v2016.xlsx', path_out='./csv_data/fips_all_codes.csv',
                         write_df=True)

# ******************************************************** #

# Testing if all the code works as expected using a sample feature
# ******************************************************** #
# read csv data
data = pd.read_csv('./csv_data/data.csv', low_memory=False, dtype=str)
excel_doc_df = pd.read_csv('./csv_data/excel_doc.csv', low_memory=False, dtype=str)
fips_all_codes_df = pd.read_csv('./csv_data/fips_all_codes.csv', low_memory=False, dtype=str)
fips_state_codes_df = pd.read_csv('./csv_data/fips_state_codes.csv', low_memory=False, dtype=str)

# feature eng
feature_df = feature_engg.get_features(data=data, doc_df=excel_doc_df, count_unique_feature_values=2)

# features can be selected selected effectively using interactive jupyter notebooks
feature = 'f1419515'
plt_title = feature_df[feature_df.field == feature]['variable_name'].tolist()[0]
plt_desc = ''
for key, value in feature_df[feature_df.field == feature].to_dict().items():
    if key in ['year_of_data', 'date_on', 'characteristics']:
        plt_desc += key+": "+str(list(value.values())[0])+"\n"

# extract data
feature_values_dict_country = feature_engg.extract_feature_data(data=data, feature=feature, state='All',
                                                                level='county')
feature_values_dict_state = feature_engg.extract_feature_data(data=data, feature=feature, state='Alabama',
                                                              level='county')

# plot on the country map
plot.colour_code_usa_country(data=feature_values_dict_country, title=plt_title, desc=plt_desc, state_borders=True,
                 county_borders=True, state_names=False)

# plot on the states map
plot.colour_code_usa_state(data=feature_values_dict_state, state='Alabama', title=plt_title, desc=plt_desc)




