import sys
from hot_tub.app.gui import QApplication, TextFileReader
from hot_tub.app import read, export

if __name__ == '__main__':

    gui = QApplication(sys.argv)
    reader = TextFileReader()
    gui.exec_()
    repo_path = reader.repo_path
    thermal_bath_path = reader.thermal_path
    selected_diodes = reader.checkbox_states


    diodes = read.get_diodes(thermal_bath_path)
    tdaus = read.get_tdau_channel(repo_path).keys()
    print(f'({len(diodes)}) diodes defined in thermal bath file: {diodes}')
    print(f'({len(tdaus)}) TDAUs defined in .soc file: {tdaus}')
    print(f'{selected_diodes}')

    diodes_input = ['NAC', 'GPIO']
    diode_to_tdau_map = {'NAC':'THERMD_TD1', 'GPIO':'THERMD_TD5'}
    temps = [-30, 80]

    tdau_data = read.create_diode_temp_dict_list(temps, diodes_input, repo_path, thermal_bath_path, diode_to_tdau_map)
    export.write_setup_file('grr', tdau_data)