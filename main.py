"""
Get employment data in csv format from the original basque labour fource data source "lanbide.eus"
An example:
    lanbide.euskadi.eus/contenidos/estadistica/datos_demanda_empleo_2020/es_def/adjuntos/10-Octubre/data_20013.csv
    lanbide.euskadi.eus/general/-/estadistica/principales-colectivos-de-la-demanda-por-municipio-y-ramas-de-actividad-durante-el-{YEAR}}/
"""
import os

import requests


def get_lanbide_data():
    local_path = 'raw_data'

    month_number_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    month_name_list = [
        'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre',
        'Diciembre']

    year_month_list = \
        [('2018', month_num, month_name) for month_num, month_name in
         list(zip(month_number_list[11:12], month_name_list[11:12]))] + \
        [('2019', month_num, month_name) for month_num, month_name in
         list(zip(month_number_list[11:12], month_name_list[11:12]))] + \
        [('2020', month_num, month_name) for month_num, month_name in
         list(zip(month_number_list[9:10], month_name_list[9:10]))]

    th_code = {'ara': '01', 'gip': '20', 'biz': '48'}

    ara_mun_list = [
        '001', '002', '003', '004', '006', '008', '009', '010', '011', '013', '014', '016', '017', '018',
        '019', '020', '021', '022', '023', '027', '028', '030', '031', '032', '033', '034', '036', '037',
        '039', '041', '042', '043', '044', '046', '047', '049', '051', '052', '053', '054', '055', '056',
        '057', '058', '059', '060', '061', '062', '063', '901', '902']

    gip_mun_list = [
        '001', '002', '003', '004', '005', '006', '007', '008', '009', '010', '011', '012', '013', '014',
        '015', '016', '017', '018', '019', '020', '021', '022', '023', '024', '025', '026', '027', '028',
        '029', '030', '031', '032', '033', '034', '035', '036', '037', '038', '039', '040', '041', '042',
        '043', '044', '045', '046', '047', '048', '049', '050', '051', '052', '053', '054', '055', '056',
        '057', '058', '059', '060', '061', '062', '063', '064', '065', '066', '067', '068', '069', '070',
        '071', '072', '073', '074', '075', '076', '077', '078', '079', '080', '081', '901', '902', '903',
        '904', '905', '906', '907']

    biz_mun_list = [
        '001', '002', '003', '004', '005', '006', '007', '008', '009', '010', '011', '012', '013', '014', '015', '016',
        '017', '018', '019', '020', '021', '022', '023', '024', '025', '026', '027', '028', '029', '030', '031', '032',
        '033', '034', '035', '036', '037', '038', '039', '040', '041', '042', '043', '044', '045', '046', '047', '048',
        '049', '050', '051', '052', '053', '054', '055', '056', '057', '058', '059', '060', '061', '062', '063', '064',
        '065', '066', '067', '068', '069', '070', '071', '072', '073', '074', '075', '076', '077', '078', '079', '080',
        '081', '082', '083', '084', '085', '086', '087', '088', '089', '090', '091', '092', '093', '094', '095', '096',
        '097', '901', '902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914',
        '915']

    mun_list = [th_code['ara'] + mun for mun in ara_mun_list] + \
               [th_code['gip'] + mun for mun in gip_mun_list] + \
               [th_code['biz'] + mun for mun in biz_mun_list]

    # Create folder in which files will be stored
    if not os.path.exists(local_path):
        os.makedirs(local_path)

    for year, month_num, month_name in year_month_list:
        for mun_code in mun_list:
            target_url = '/'.join(
                (
                    'https://www.lanbide.euskadi.eus/contenidos/estadistica',
                    'datos_demanda_empleo_' + year,
                    'es_def/adjuntos',
                    '-'.join((month_num, month_name)),
                    'data_' + mun_code + '.csv'
                )
            )
            target_filepath = '/'.join((local_path, '_'.join((year, month_num, mun_code)) + '.csv'))
            if not os.path.isfile(target_filepath):
                r = requests.get(target_url)
                if r.status_code == 404:
                    print("ERROR 404: " + target_filepath + " | Could not find data at: " + target_url)
                else:
                    with open(target_filepath, 'wb') as f:
                        f.write(r.content)
                        print(target_filepath + " - created")
            else:
                print("EXISTS already: " + target_filepath)


if __name__ == '__main__':
    get_lanbide_data()
