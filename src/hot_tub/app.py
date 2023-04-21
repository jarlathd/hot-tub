'''
Builds GUI
Reads user input and exports tdau setup xml
'''
from hot_tub import read, export
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton
from PyQt5.QtGui import QIcon
import sys

class FileSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.repo_path = ''
        self.thermal_bath_path = ''
        self.initUI()

    def initUI(self):
        self.setWindowTitle('File Selector')
        self.setGeometry(100, 100, 500, 300)

        # Create two buttons to select repository and thermal file paths
        repo_button = QPushButton('Select product repo root directory', self)
        repo_button.setGeometry(50, 50, 200, 50)
        repo_button.clicked.connect(self.select_repo_path)

        thermal_button = QPushButton('Select thermal bath File', self)
        thermal_button.setGeometry(50, 150, 200, 50)
        thermal_button.clicked.connect(self.select_thermal_bath_path)

        self.show()

    def select_repo_path(self):
        # Open file dialog to select repository path
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.Directory) # set file mode to directory only
        self.repo_path = file_dialog.getExistingDirectory(self, 'Select Repository Path')
        print('Selected rep root directory:', self.repo_path)

    def select_thermal_bath_path(self):
        # Open file dialog to select thermal file path
        file_dialog = QFileDialog()
        self.thermal_bath_path, _ = file_dialog.getOpenFileName(self, 'Select Thermal File Path')
        print('Selected Thermal File Path:', self.thermal_bath_path)

if __name__ == '__main__':
    app = QApplication([])
    selector = FileSelector()
    app.exec_()
    repo_path = selector.repo_path
    thermal_bath_path = selector.thermal_bath_path
    print('Repo Path:', selector.repo_path)
    print('Thermal Bath Path:', selector.thermal_bath_path)

temps = [-30, 80]
diodes = ['NAC', 'GPIO']
diode_to_tdau_map = {'NAC':'THERMD_TD1', 'GPIO':'THERMD_TD5'}
tdau_data = read.create_diode_temp_dict_list(temps, diodes, repo_path, thermal_bath_path, diode_to_tdau_map)
export.write_setup_file('grr', tdau_data)