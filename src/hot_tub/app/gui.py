'''
GUI layer that takes user inputs which are passed to reader functions
'''

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QRadioButton, QGroupBox, QPushButton, QLabel, QLineEdit, QFileDialog
from hot_tub.app import read

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BATH TIME")
        self.setGeometry(100, 100, 500, 300)
        self.diode_group_boxes = []
        self.temp_group_boxes = []
        self.radio_buttons = []
        self.repo_path = ''
        self.thermal_path = ''
        self.tdaus = []
        self.diodes = []
        self.tdau_diode_map = {}
        self.temps = []
        self.product = ''

        central_widget = QWidget()
        self.layout = QVBoxLayout(central_widget)

        repo_button = QPushButton('Select Repository Folder', self)
        repo_button.clicked.connect(self.select_repo)
        self.layout.addWidget(repo_button)

        thermal_button = QPushButton('Select Thermal Bath File', self)
        thermal_button.clicked.connect(self.select_thermal)
        self.layout.addWidget(thermal_button)
        
        self.setCentralWidget(central_widget)
    
    def select_repo(self):
        #file_dialog = QFileDialog()
        #file_dialog.setFileMode(QFileDialog.Directory) # set file mode to directory only
        #self.repo_path = file_dialog.getExistingDirectory(self, 'Select Repository Folder')
        self.repo_path = "C:/Users/jarlathd/source/repos/grr-sort"
        print('Selected Repository Folder:', self.repo_path)

    def select_thermal(self):
        #file_dialog = QFileDialog()
        #self.thermal_path, _ = file_dialog.getOpenFileName(self, 'Select Thermal Bath File', '', 'Xlsx files (*.xlsx)')
        self.thermal_path = "C:/Users/jarlathd/source/product_data/grr_data/I310001EN_GRR-A0_PDE-PG_10-units_V=0.xlsx"
        print('Selected Thermal Bath File:', self.thermal_path)

        if self.thermal_path:
            self.read_file()
    
    def read_file(self):
        self.tdaus = list(read.get_tdau_channel(self.repo_path).keys())
        self.diodes = read.get_diodes(self.thermal_path)
        self.product = read.get_product_name(self.thermal_path)
        self.SDS_temps, self.SDT_temps   = read.get_temps(self.thermal_path)

        central_widget = self.centralWidget()
        layout = central_widget.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        for tdau in self.tdaus:
            group_box = QGroupBox(tdau)
            self.diode_group_boxes.append(group_box)
            group_box_layout = QVBoxLayout()

            for diode in self.diodes:
                radio_button = QRadioButton(diode)
                self.radio_buttons.append(radio_button)
                group_box_layout.addWidget(radio_button)

            group_box.setLayout(group_box_layout)
            self.layout.addWidget(group_box)
        
        group_box = QGroupBox(f'Select SDS temperature')
        self.temp_group_boxes.append(group_box)
        group_box_layout = QVBoxLayout()
        for temp in self.SDS_temps:
            radio_button = QRadioButton(f'{temp}')
            self.radio_buttons.append(radio_button)
            group_box_layout.addWidget(radio_button)
        group_box.setLayout(group_box_layout)
        self.layout.addWidget(group_box)

        group_box = QGroupBox(f'Select SDT temperature')
        self.temp_group_boxes.append(group_box)
        group_box_layout = QVBoxLayout()
        for temp in self.SDT_temps:
            radio_button = QRadioButton(f'{temp}')
            self.radio_buttons.append(radio_button)
            group_box_layout.addWidget(radio_button)
        
        group_box.setLayout(group_box_layout)
        self.layout.addWidget(group_box)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submitSelection)
        self.layout.addWidget(submit_button)

        self.setLayout(self.layout)
        self.show()

    def submitSelection(self):
        for i, group_box in enumerate(self.diode_group_boxes):
            selected_diode_button = ""
            for j, radio_button in enumerate(group_box.findChildren(QRadioButton)):
                if radio_button.isChecked():
                    selected_diode_button = self.diodes[j]
                    break
            self.tdau_diode_map[self.tdaus[i]] = selected_diode_button
        
        for x, group_box in enumerate(self.temp_group_boxes):
            if x == 0:
                selected_SDS_button = ""
                for y, radio_button in enumerate(group_box.findChildren(QRadioButton)):
                    if radio_button.isChecked():
                        selected_SDS_button = self.SDS_temps[y]
                        break
            else:
                selected_SDT_button = ""
                for y, radio_button in enumerate(group_box.findChildren(QRadioButton)):
                    if radio_button.isChecked():
                        selected_SDT_button = self.SDT_temps[y]
                        break
        
        self.temps = [selected_SDS_button, selected_SDT_button]

        print(self.tdau_diode_map)
        print(self.temps)
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())