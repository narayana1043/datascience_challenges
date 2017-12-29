import xlrd
import re
import pandas as pd


def read_sas_doc(path_in, path_out, return_df=False, write_df=False):
    """
    Reads the SAS document and return a processed data frame containing all the information in the SAS document. The
     SAS file is missing some information that is present in excel document. At this point I don't see that information
     relevant.
    :param path_out: where to output the csv file
    :param path_in: location of the file
    :param write_df: writes data frame to disk 'path: ./DATA/docs_df.csv'
    :param return_df: if True returns a data frame
    :return: None or data frame: if return_df - True)
    """

    if not write_df and not return_df:
        raise Exception('Choose proper parameters to read the docs')

    with open(path_in, 'r') as f:
        i = 0
        labels = []
        for line in f:
            i += 1
            if 6 < i < 6816:
                label_dict = {'field': line[15:23].strip(),
                              'field_variable_name': line[34:65].strip(),
                              'field_variable_characteristics': line[68:104].strip(),
                              'field_start_index': int(line[6:11].lstrip('0')) - 1}
                labels.append(label_dict)

    sas_doc_df = pd.DataFrame(data=labels)
    sas_doc_df = sas_doc_df[[col for col in labels[0].keys()]]
    sas_doc_df['field_end_index'] = sas_doc_df['field_start_index'].shift(-1).fillna(value=31492).astype(int)
    print(sas_doc_df.head())

    if write_df:
        sas_doc_df.to_csv(path_out, index=False)

    if return_df:
        return sas_doc_df

    return None


def read_data_wrt_sas_docs(path_in, path_out, return_df=False, write_df=False):
    """
    reads the ahrf data w.r.t to the sas doc avaiable
    :param path_in: location of the arhf data file
    :param path_out: where to out put the csv file
    :param return_df: Boolean if true reutrns the data as df else None
    :param write_df: Boolean if ture writes the data into the path_out specified
    :return: id return_df is true it returns data frame.
    """
    if not write_df and not return_df:
        raise Exception('Choose proper parameters to read the docs')

    docs_df = pd.read_csv('./csv_data/sas_doc.csv', header='infer')
    with open(path_in, 'r') as f:
        field_start_index_list = docs_df['field_start_index'].tolist()
        field_list = docs_df['field'].tolist()
        field_end_index_list = docs_df['field_end_index'].tolist()
        data = []
        for line in f.readlines():
            record = {}
            for fn, si, ei in zip(field_list, field_start_index_list, field_end_index_list):
                record[fn] = str(line[si:ei]).strip()

            data.append(record)

    data_df = pd.DataFrame(data)

    # print(len(data_df.columns))

    if write_df:
        data_df.to_csv(path_out, index=False)

    if return_df:
        return data_df

    return None


def read_excel_doc(path_in, path_out, return_df=False, write_df=False):
    """
    read the data from excel doc and converts it into csv file
    :param path_in location of the excel document
    :param path_out where to write the csvoutput file to
    :param return_df: Boolean if true returns data frame
    :param write_df: Boolean writes data frame if true
    :return: returns data frame or None
    """
    work_book = xlrd.open_workbook(path_in)
    work_sheet = work_book.sheet_by_name('AHRF 2016-17 Technical Doc')
    labels = []
    col_name_list = ['field', 'col_col', 'year_of_data', 'variable_name', 'characteristics', 'source', 'date_on']

    for row in range(184, 7890):
        value = work_sheet.cell_value(row, 0).strip()
        if re.match(pattern='^F[0-9][0-9]', string=value) is not None:
            labels_dict = {}
            for col, col_name in zip(range(7), col_name_list):
                value = str(work_sheet.cell_value(row, col)).strip()
                labels_dict[col_name] = value
            labels.append(labels_dict)

    excel_doc_df = pd.DataFrame(labels)
    excel_doc_df = excel_doc_df[[col_name for col_name in col_name_list]]
    excel_doc_df['field'] = excel_doc_df['field'].str.lower().str.replace('-', '')
    # print(excel_doc_df.head())
    # print(excel_doc_df.tail())
    # print(excel_doc_df.count())

    if write_df:
        excel_doc_df.to_csv(path_out, index=False)

    if return_df:
        return excel_doc_df

    return None


def read_fips_state_codes(path_in, path_out, write_df=False, return_df=False):
    """
    reads states FIP code file and writes it into csv file ar returns a data frame based the parametes set
    :param path_in input path of the file
    :param path_out out path to wrrite the data as csv
    :param write_df Boolean if true writes csv file
    :param return_df Boolean if true returns a dataframe
    :return: FIP codes returns data frame or None
    """
    if not write_df and not return_df:
        raise Exception('Choose proper parameters to read the docs')

    fip_codes_df = pd.read_csv(path_in, sep='|', header='infer', dtype=str)

    # print(fip_codes_df.head())
    if write_df:
        fip_codes_df.to_csv(path_out, index=False)

    if return_df:
        return fip_codes_df


def read_fips_all_codes(path_in, path_out, write_df=False, return_df=False):
    """
    reads all FIP (state & county) code file and writes it into csv file ar returns a data frame based the parametes set
    :param path_in input path of the file
    :param path_out out path to wrrite the data as csv
    :param write_df Boolean if true writes csv file
    :param return_df Boolean if true returns a dataframe
    :return: FIP codes returns data frame or None
    """
    if not write_df and not return_df:
        raise Exception('Choose proper parameters to read the docs')

    work_book = xlrd.open_workbook(path_in)
    work_sheet = work_book.sheet_by_name('Sheet1')
    labels = []
    col_name_list = ['summary_level', 'state_code', 'county_code', 'county_subdivision', 'place_code',
                     'consolidated_city_code', 'area_name']

    for row in range(5, 43939):
        labels_dict = {}
        for col, col_name in zip(range(7), col_name_list):
            value = str(work_sheet.cell_value(row, col)).strip()
            labels_dict[col_name] = value
        labels.append(labels_dict)

    excel_doc_df = pd.DataFrame(labels, dtype=str)
    excel_doc_df = excel_doc_df[[col_name for col_name in col_name_list]]

    if write_df:
        excel_doc_df.to_csv(path_out, index=False)

    if return_df:
        return excel_doc_df

    return None
