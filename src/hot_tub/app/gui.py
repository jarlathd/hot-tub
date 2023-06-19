'''
Builds GUI
Reads user input and exports tdau setup xml
'''
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QPushButton, QCheckBox, QVBoxLayout, QWidget
from hot_tub.app import read

class TextFileReader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.repo_path = ''
        self.thermal_path = ''
        self.tdaus = []
        self.diodes = []
        self.checkbox_states = {}
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Bath Time')
        self.setGeometry(100, 100, 500, 300)

        # Create two buttons to select repository and thermal file paths
        repo_button = QPushButton('Select Repository Folder', self)
        repo_button.setGeometry(50, 50, 200, 50)
        repo_button.clicked.connect(self.select_repo_path)

        thermal_button = QPushButton('Select Thermal Bath File', self)
        thermal_button.setGeometry(50, 150, 200, 50)
        thermal_button.clicked.connect(self.select_thermal_path)

        # Create a layout for the buttons
        buttons_layout = QVBoxLayout()

        # Create a widget to hold the layout
        buttons_widget = QWidget()
        buttons_widget.setLayout(buttons_layout)

        # Set the widget as the central widget of the main window
        self.setCentralWidget(buttons_widget)

        buttons_layout.addWidget(repo_button)
        buttons_layout.addWidget(thermal_button)

        self.show()

    def select_repo_path(self):
        # Open file dialog to select repository path
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.Directory) # set file mode to directory only
        self.repo_path = file_dialog.getExistingDirectory(self, 'Select Repository Folder')
        print('Selected Repository Folder:', self.repo_path)

    def select_thermal_path(self):
        # Open file dialog to select thermal file path
        file_dialog = QFileDialog()
        self.thermal_path, _ = file_dialog.getOpenFileName(self, 'Select Thermal Bath File', '', 'Xlsx files (*.xlsx)')
        print('Selected Thermal Bath File:', self.thermal_path)

        self.tdaus = read.get_tdau_channel(self.repo_path).keys()
        self.diodes = read.get_diodes(self.thermal_path)

        buttons_layout = self.centralWidget().layout()
        for tdau in self.tdaus:
            label_widget = QLabel(tdau, self)
            buttons_layout.addWidget(label_widget)
            for diode in self.diodes:
                button = QCheckBox(diode, self)
                button.stateChanged.connect(lambda state, tdau=tdau, diode=diode: self.update_checkbox_state(state, tdau, diode))
                buttons_layout.addWidget(button)

    def update_checkbox_state(self, state, tdau, diode):
        if tdau not in self.checkbox_states:
            self.checkbox_states[tdau] = {}
        self.checkbox_states[tdau][diode] = state