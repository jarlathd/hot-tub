"""
Gets data from .soc and Thermal Bath file
"""
import glob
import re
import pandas as pd
from itertools import chain

def read_soc_file(repo_path):
    for file_path in glob.iglob(f'{repo_path}\\**\\*.soc', recursive=True):
        with open(file_path, 'rt') as socfile:
            return socfile.read()
    return None

def get_tdau_channel(repo_path):
    socfile = read_soc_file(repo_path)
    matches = re.findall(r'Resource TDAU\n\s*{\n\s*(.*?)\n\s*}', socfile, re.DOTALL)

    tdau_dict = {}
    for match in matches:
        for line in match.split('\n'):
            line = line.strip()
            if line:
                key, value = line.split()
                value = value.split('.')[1]
                value = value.replace(';', '')
                tdau_dict[key] = value
    
    return tdau_dict

def get_product_name(tb_path):
    df = pd.read_excel(tb_path, sheet_name='Info')
    df.columns = range(df.shape[1])
    product = df.iloc[5, 1].replace(" ", "_")
    return product

def read_thermal_bath_summary(tb_path):
    summary_df = pd.read_excel(tb_path, sheet_name='Summary')
    return summary_df

def extract_dataframe(df, keyword):
    start_idx = df[df['Summary Data'].str.contains(keyword, na=False)].index[0]
    end_idx = df[start_idx+1:].index[df[start_idx+1:].isnull().all(axis=1)][0]
    result = df.iloc[start_idx:end_idx, :]
    result.reset_index(drop=True, inplace=True)
    result.columns = result.iloc[0]
    result = result[1:]
    result.dropna(axis='columns', inplace=True)
    return result

def get_diodes(tb_path):
    df_summary = read_thermal_bath_summary(tb_path)
    df = extract_dataframe(df_summary, 'Diode Equation Per Sourcing Current')
    diodes = df.columns.tolist()
    diodes.pop(0)
    diodes = [i.strip('Diode ') for i in diodes]
    return diodes

def get_temps(tb_path):
    df_summary = read_thermal_bath_summary(tb_path)
    df = extract_dataframe(df_summary, '3-Currents')
    temps = df.iloc[:,[1]].values.tolist()
    temps = sorted(set(sum(temps, [])))
    SDS_temps = [i for i in temps if i <= 0]
    SDT_temps = [i for i in temps if i > 0]
    return SDS_temps, SDT_temps

def get_slope(df, diode):
    s = df.filter(regex=diode)
    equation = s.values[0]
    slope = equation.tolist()
    slope = slope[0].split('Vbe')
    slope = slope[0]
    return slope

def get_ncurrent_ideality(df, diode, temp):
    idx = (df.iloc[:,0].str.contains(diode)) & (df.iloc[:,1] == temp)
    ideality = df.loc[idx, df.columns[5]].values[0]
    currents = df.loc[idx, df.columns[0]].values[0]
    ncurrents = re.findall('=\d*.A', currents)
    ncurrents = [re.sub(r'\D', '', value) for value in ncurrents]
    return ncurrents, ideality

def create_diode_temp_dict(repo_path, tb_path, tdau, temp, map):
    diode = map[tdau]
    tdau_channel_dict = get_tdau_channel(repo_path)
    channel = tdau_channel_dict[tdau]

    df_summary = read_thermal_bath_summary(tb_path)
    df_ideality = extract_dataframe(df_summary, '3-Currents')
    df_slope = extract_dataframe(df_summary, 'Diode Equation Per Sourcing Current')
    ncurrents, ideality = get_ncurrent_ideality(df_ideality, diode, temp)
    slope = get_slope(df_slope, diode)
    
    tdau_data = {   'diode'    : diode, 
                    'tdau'     : tdau,
                    'channel'  : channel,
                    'slope'    : slope,
                    'temp'     : temp, 
                    'current'  : ncurrents,  
                    'ideality' : ideality}    
    
    return tdau_data

def create_diode_temp_dict_list(temps, tdaus, soc_path, tb_path, tdau_diode_map):
    tdau_data_wrapped = []
    for temp in temps:
        for tdau in tdaus:
                tdau_data = create_diode_temp_dict(soc_path, tb_path, tdau, temp, tdau_diode_map)
                tdau_data_wrapped.append(tdau_data)
    return tdau_data_wrapped

























        












