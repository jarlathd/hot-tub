import sys
from hot_tub.app.gui import QApplication, MainWindow
from hot_tub.app import read, export

if __name__ == '__main__':
    app = QApplication(sys.argv)
    reader = MainWindow()
    reader.show()
    app.exec_()

    tdau_data = read.create_diode_temp_dict_list(reader.temps, reader.tdaus, reader.repo_path, reader.thermal_path, reader.tdau_diode_map)
    export.write_setup_file(reader.product, tdau_data)