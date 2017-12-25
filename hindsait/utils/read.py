import pandas as pd
import xlrd
import re

def read_sas_doc(return_df=False, write_df=False):
    """
    Reads the SAS document and return a processed data frame containing all the information in the SAS document. The
     SAS file is missing some information that is present in excel document. At this point I don't see that information
     relevant.
    :param write_df: writes data frame to disk 'path: ./DATA/docs_df.csv'
    :param return_df: if True returns a data frame
    :return:
    """

    if not write_df and not return_df:
        raise Exception('Choose proper parameters to read the docs')

    with open('../DOC/ahrf2016-17.sas', 'r') as f:
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
        sas_doc_df.to_csv('../DATA/sas_doc.csv', index=False)

    if return_df:
        return sas_doc_df

    return None


def read_data_wrt_sas_docs(return_df=False, write_df=False):
    """

    :param return_df:
    :param write_df:
    :return:
    """
    if not write_df and not return_df:
        raise Exception('Choose proper parameters to read the docs')

    with open('../DATA/ahrf2017.asc', 'r') as f:

        try:
            docs_df = pd.read_csv(filepath_or_buffer='../DATA/sas_doc.csv', header='infer')
        except IOError:
            docs_df = read_sas_doc(write_df=True, return_df=True)

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

    print(len(data_df.columns))

    if write_df:
        data_df.to_csv('../DATA/data.csv', index=False)

    if return_df:
        return data_df

    return None


def read_excel_doc(return_df=False, write_df=False):
    """

    :param return_df:
    :param write_df:
    :return:
    """
    work_book = xlrd.open_workbook('../DOC/AHRF 2016-2017 Technical Documentation.xlsx')
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
    # print(excel_doc_df.head())
    # print(excel_doc_df.tail())
    # print(excel_doc_df.count())

    if write_df:
        excel_doc_df.to_csv('../DATA/excel_doc.csv', index=False)

    if return_df:
        return excel_doc_df

    return None


def read_fips_codes(write_df=False, return_df=False):
    """

    :return: FIP codes data frame
    """
    if not write_df and not return_df:
        raise Exception('Choose proper parameters to read the docs')

    url = 'https://www2.census.gov/geo/docs/reference/state.txt'
    fip_codes_df = pd.read_csv(url, sep='|', header='infer')

    print(fip_codes_df.head())
    if write_df:
        fip_codes_df.to_csv('../DATA/fips_state_codes.csv', index=False)

    if return_df:
        return fip_codes_df


# read_sas_doc(write_df=True)
# read_data_wrt_sas_docs(write_df=True)
# read_excel_doc(write_df=True)
# read_fips_codes(write_df=True)

# df = pd.read_csv('../DATA/doc.csv')
# print(df.count())
# print(df[df['field_length']>30].count())
# print(df[df['field_length']>30][['field_variable_name']].head())

# df = pd.read_csv('../DATA/data.csv')
# print(len(df.columns))
# for col in df.columns:
#     print(col)
# print(df[['f1389115', 'f1389215']].head())
