import wget
import zipfile
import os
from git import Repo


def download_data():
    """

    :return:
    """
    wget.download('https://datawarehouse.hrsa.gov/DataDownload/AHRF/AHRF_2016-2017.ZIP')
    zipfile.ZipFile('AHRF_2016-2017.ZIP', 'r').extractall('./')
    os.remove('AHRF_2016-2017.ZIP')
    wget.download('https://www2.census.gov/geo/docs/reference/state.txt', out='./DATA/')
    wget.download('https://www2.census.gov/programs-surveys/popest/geographies/2016/all-geocodes-v2016.xlsx',
                  out='./DATA/')

    return 0


def download_vincent_data():
    """

    :return:
    """
    if not os.path.exists('./vincent_map_data'):
        Repo.clone_from(url='https://github.com/wrobstory/vincent_map_data', to_path='./vincent_map_data/')
    else:
        print('path exists "./vincent_map_data" check files')
    return 0



def download_us_shape_files(resolution='low', path_out='./basemaps/'):
    """

    :param resolution: str: 'low' 500k, 'medium' 5m, 'high' 20m
    :param path_out:
    :return:
    """
    for file in os.listdir(path_out):
        os.remove(path_out+file)

    base_map_url = 'http://www2.census.gov/geo/tiger/GENZ2016/shp/'

    if resolution == 'low':
        county_url = 'cb_2016_us_county_500k.zip'
        state_url = 'cb_2016_us_state_500k.zip'
    elif resolution == 'medium':
        county_url = 'cb_2016_us_county_5m.zip'
        state_url = 'cb_2016_us_state_5m.zip'
    elif resolution == 'high':
        county_url = 'cb_2016_us_county_20m.zip'
        state_url = 'cb_2016_us_state_20m.zip'

    wget.download(base_map_url + county_url)
    zipfile.ZipFile(county_url, 'r').extractall(path=path_out)
    os.remove(county_url)
    wget.download(base_map_url + state_url)
    zipfile.ZipFile(state_url, 'r').extractall(path=path_out)
    os.remove(state_url)

    return 0


def create_dirs(dir_list=[]):
    """

    :param dir_list:
    :return:
    """
    for dir in dir_list:
        if not os.path.exists(dir):
            os.mkdir(path=dir)