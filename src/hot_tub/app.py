'''
Builds GUI
Reads user input and exports tdau setup xml
'''

from hot_tub import read, export

#TODO: GUI goes here

#Dummy values for testing
soc_path = 'C:\\Users\\jarlathd\\source\\repos\\grr-sort'
tb_path = 'C:\\Users\\jarlathd\\source\\product_data\\grr_data\\I310001EN_GRR-A0_PDE-PG_10-units_V=0.xlsx'
temps = [-30, 80]
diodes = ['NAC', 'GPIO']
diode_to_tdau_map = {'NAC':'THERMD_TD1', 'GPIO':'THERMD_TD5'}
tdau_data = read.create_diode_temp_dict_list(temps, diodes, soc_path, tb_path, diode_to_tdau_map)
export.write_setup_file('grr', tdau_data)