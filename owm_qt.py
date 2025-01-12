"""
    Name: owm_gui.py
    Author: William A Loring
    Created: 08-05-2021
    Purpose: OpenWeatherMap GUI with PySide6
    stick with pyside6 for nuitka
    Command line to rebuild ui to py
    pyside6-uic main_window.ui -o main_ui.py
"""

import sys
from os import path
from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu
from base64 import b64decode
# Import gui py file created by QT Designer
from main_ui import Ui_MainWindow
# Import controller class
from owm_class import WeatherClass
from weather_icon import large_icon_data


class OWM(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(OWM, self).__init__()
        self.initializeUI()
        # Create weather object with a reference to current class
        self.weather_class = WeatherClass(self)

        # Connect the clicked event/signal to the get_location event handler/slot
        self.btn_get_weather.clicked.connect(self.weather_class.get_location)

        # Exit the program
        self.btn_exit.clicked.connect(self.close)
        self.action_exit.triggered.connect(self.close)
        self.btn_exit.setShortcut("Escape")

        self.action_about.triggered.connect(self.weather_class.about_program)
        self.action_get_weather.triggered.connect(
            self.weather_class.get_location)

        # Remove sizing grip from status bar
        self.status_bar.setSizeGripEnabled(False)

        # Set window title bar icon, shows in task bar
        my_icon = QIcon()
        # Load and decode base64 icon data
        cloudy = b64decode(large_icon_data)
        pixmap = QPixmap()
        pixmap.loadFromData(cloudy)
        my_icon.addPixmap(pixmap)

        self.setWindowIcon(my_icon)

        # Add progress bar to status bar
        self.status_bar.addPermanentWidget(self.progress_bar)
        # Set statusbar tips
        self.btn_get_weather.setStatusTip("Get current weather (Press Enter)")
        self.btn_exit.setStatusTip("Exit Program (Press Esc)")
        self.lineEdit.setStatusTip(
            "Enter Town, State, Country (Scottsbluff, NE, US)")

        # Select the input box
        # Wait for the user to click Get Weather or press Return
        self.set_input()

# --------------------- INITIALIZE UI -------------------------------------#
    def initializeUI(self):
        """ Initialize PySide6 QT GUI"""
        # Create the GUI
        self.setupUi(self)
        # Remove title bar
        self.setWindowFlag(Qt.FramelessWindowHint)
        # Don't allow window to be resized
        self.setFixedSize(self.size())

# --------------------- SETUP CONTEXT MENU --------------------------------#
    def contextMenuEvent(self, event):
        """Override the contextMenuEvent
            Setup a context or right click menu
        """
        # Creating a menu object with the central widget as parent
        menu = QMenu(self)
        # Populating the menu with actions defined in init
        menu.addAction(self.action_about)
        menu.addAction(self.action_get_weather)
        menu.addAction(self.action_exit)
        # Launching the menu
        menu.exec(event.globalPos())

# --------------------- SELECT INPUT --------------------------------------#
    def set_input(self):
        """ Set focus and select lineEdit, wait for user input"""
        self.lineEdit.setFocus()
        self.lineEdit.selectAll()
        self.progress_bar.setValue(0)

# --------------------- GET WEATHER ---------------------------------------#
    def get_weather(self):
        """ Get and display weather on form """
        self.progress_bar.setValue(33)
        self.weather_class.get_dictionaries()
        self.weather_class.get_weather()
        self.weather_class.draw_weather_arrow()
        self.progress_bar.setValue(66)
        self.weather_class.display_weather()
        self.progress_bar.setValue(100)
        # Set focus and select lineEdit for next user entry
        self.lineEdit.setFocus()
        self.lineEdit.selectAll()

# -------- OVERRIDE MOUSE EVENTS TO MOVE PROGRAM WINDOW -------------------#
    def mousePressEvent(self, event):
        """ Override the mousePressEvent """
        # Store the current position of the mouse in previous position
        self.previous_pos = event.globalPosition()

    def mouseMoveEvent(self, event):
        """ Override the mouseMoveEvent """
        # Subtract the previous position from the current position
        delta = event.globalPosition() - self.previous_pos
        # Add the delta calculation to the current position
        self.move(self.x() + delta.x(), self.y()+delta.y())
        # Store the current position
        self.previous_pos = event.globalPosition()
        # self._drag_active = True

# -------- OVERRIDE KEYPRESS EVENTS TO CAPTURE KEYSTROKES -----------------#
    # Overide the keyPressEvent
    def keyPressEvent(self, event):
        # Get location for weather
        if event.key() == QtCore.Qt.Key_Enter or QtCore.Qt.Key_Return:
            self.weather_class.get_location()


# --------------------- START APPLICATION ---------------------------------#
# Create application object
owm = QApplication(sys.argv)

# Determine the path to the stylesheet
if getattr(sys, 'frozen', False):
    # If the application is frozen (compiled with Nuitka)
    base_path = sys._MEIPASS
else:
    # If the application is running in a normal Python environment
    base_path = path.dirname(path.abspath(__file__))

style_path = path.join(base_path, "Darkeum.qss")

# Open external stylesheet and read it
with open(style_path, "r") as f:
    style = f.read()
    # Apply the style sheet to the application
    owm.setStyleSheet(style)

# Create program object
window = OWM()

# Make program visible
window.show()

# Set colors to darkPalette, from external py file
#    owm.setPalette(dark_palette.darkPalette)
# Execute the program, setup clean exit of program
sys.exit(owm.exec())
