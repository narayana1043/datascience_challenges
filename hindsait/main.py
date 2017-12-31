from utils import download
from utils.read import ReadFiles
from utils import plot
import pandas as pd
import feature_engg

def main(get_files = False):

    if get_files == True:
        dir_list = ['./csv_data/',
                    # './vincent_map_data/',
                    './basemaps/']

        # below code is not required once the files are downloaded and processed
        # ********************************************************************** #
        # get data
        download.download_data()
        download.create_dirs(dir_list)
        download.download_us_shape_files(resolution='low')

        # pre-processing/parsing
        read_doc = ReadFiles(path_in='./DOC/', path_out='./csv_data/')
        read_doc.read_sas_doc(write_df=True)
        read_doc.read_excel_doc(write_df=True)

        read_data = ReadFiles(path_in='./DATA/', path_out='./csv_data/')
        read_data.read_data_wrt_sas_docs(write_df=True)
        read_data.read_fips_state_codes(write_df=True)
        read_data.read_fips_all_codes(write_df=True)

    # ******************************************************** #
    # Testing if all the code works as expected using a sample feature
    # ******************************************************** #
    # read csv data
    data = pd.read_csv('./csv_data/data.csv', low_memory=False, dtype=str)
    excel_doc_df = pd.read_csv('./csv_data/excel_doc.csv', low_memory=False, dtype=str)

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
    feature_values_dict_country = feature_engg.extract_feature_data(data=data, feature=feature, state='All')
    feature_values_dict_state = feature_engg.extract_feature_data(data=data, feature=feature, state='CA')

    US_map = plot.USMaps(state_borders=True,county_borders=True, state_names=False)

    US_map.colour_code_usa_country(data=feature_values_dict_country, title=plt_title, desc=plt_desc)

    US_map.colour_code_usa_state(data=feature_values_dict_state, state='CA', title=plt_title, desc=plt_desc)



if __name__ == "__main__":

    # if your running the code for the first time set the variable get files to True to download the files.
    main(get_files=False)
