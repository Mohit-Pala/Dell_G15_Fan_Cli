#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dell G15 GUI Controller
A PyQt6 dashboard to monitor system stats and control fan modes by calling the g15-fan-cli.py script.
"""

import sys
import subprocess
import psutil
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFrame, QGridLayout)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QIcon, QFont

# --- CONFIGURATION ---
# This path has been updated to the correct location you specified.
G15_CLI_SCRIPT_PATH = "/home/biswas/.local/bin/g15-fan-cli.py"
# ---------------------


class G15ControlGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.update_stats()

    def init_ui(self):
        """Initializes the user interface."""
        self.setWindowTitle("Dell G15 Control")
        self.setWindowIcon(self.get_icon())
        self.setFixedSize(400, 390) # Increased height for the new field

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        self.setLayout(main_layout)

        # --- Stats Display ---
        stats_frame = QFrame()
        stats_frame.setFrameShape(QFrame.Shape.StyledPanel)
        stats_layout = QGridLayout(stats_frame)
        stats_layout.setSpacing(10)

        # Labels for stats
        self.cpu_temp_label = self.create_stat_label("CPU Temp:")
        self.ram_usage_label = self.create_stat_label("RAM Usage:")
        self.fan1_speed_label = self.create_stat_label("Fan 1 (CPU):")
        self.fan2_speed_label = self.create_stat_label("Fan 2 (GPU):")
        self.battery_health_label = self.create_stat_label("Battery Health:")
        
        # Values for stats
        self.cpu_temp_value = self.create_value_label("N/A")
        self.ram_usage_value = self.create_value_label("N/A")
        self.fan1_speed_value = self.create_value_label("N/A")
        self.fan2_speed_value = self.create_value_label("N/A")
        self.battery_health_value = self.create_value_label("N/A")
        
        # Add widgets to grid layout
        stats_layout.addWidget(self.cpu_temp_label, 0, 0)
        stats_layout.addWidget(self.cpu_temp_value, 0, 1)
        stats_layout.addWidget(self.ram_usage_label, 1, 0)
        stats_layout.addWidget(self.ram_usage_value, 1, 1)
        stats_layout.addWidget(self.fan1_speed_label, 2, 0)
        stats_layout.addWidget(self.fan1_speed_value, 2, 1)
        stats_layout.addWidget(self.fan2_speed_label, 3, 0)
        stats_layout.addWidget(self.fan2_speed_value, 3, 1)
        stats_layout.addWidget(self.battery_health_label, 4, 0)
        stats_layout.addWidget(self.battery_health_value, 4, 1)

        main_layout.addWidget(stats_frame)

        # --- Control Buttons ---
        button_frame = QFrame()
        button_frame.setFrameShape(QFrame.Shape.StyledPanel)
        button_layout = QVBoxLayout(button_frame)
        
        g_mode_button = QPushButton("Toggle G-Mode (Game Shift)")
        g_mode_button.setObjectName("g_mode")
        g_mode_button.clicked.connect(lambda: self.run_cli_command('g'))

        other_buttons_layout = QHBoxLayout()
        perf_button = QPushButton("Performance")
        perf_button.clicked.connect(lambda: self.run_cli_command('p'))
        
        balanced_button = QPushButton("Balanced")
        balanced_button.clicked.connect(lambda: self.run_cli_command('b'))
        
        quiet_button = QPushButton("Quiet")
        quiet_button.clicked.connect(lambda: self.run_cli_command('q'))

        other_buttons_layout.addWidget(perf_button)
        other_buttons_layout.addWidget(balanced_button)
        other_buttons_layout.addWidget(quiet_button)

        button_layout.addWidget(g_mode_button)
        button_layout.addLayout(other_buttons_layout)
        main_layout.addWidget(button_frame)
        
        # --- Timer to update stats every 2 seconds ---
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(2000) # 2000 milliseconds = 2 seconds

        self.apply_stylesheet()

    def create_stat_label(self, text):
        """Helper to create a consistent label for stats."""
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        return label

    def create_value_label(self, text):
        """Helper to create a consistent label for stat values."""
        label = QLabel(text)
        label.setFont(QFont("Ubuntu Mono", 12, QFont.Weight.Bold))
        return label

    def get_icon(self):
        """Creates a simple SVG icon for the window."""
        from PyQt6.QtGui import QPixmap
        from PyQt6.QtCore import QByteArray
        
        svg_data = """
        <svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
          <g transform="translate(32,32)">
            <path d="M0-28 A28 28 0 0 1 24.24 14 L12.12 7 A14 14 0 0 0 0 -14Z" fill="#3498db"/>
            <path d="M24.24 14 A28 28 0 0 1 -24.24 14 L-12.12 7 A14 14 0 0 0 12.12 7Z" fill="#3498db"/>
            <path d="M-24.24 14 A28 28 0 0 1 0 -28 L0 -14 A14 14 0 0 0 -12.12 7Z" fill="#3498db"/>
            <circle cx="0" cy="0" r="6" fill="white"/>
          </g>
        </svg>
        """
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray(svg_data.encode('utf-8')))
        return QIcon(pixmap)

    def apply_stylesheet(self):
        """Applies a dark theme stylesheet to the application."""
        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                color: #ecf0f1;
                font-family: Ubuntu;
                font-size: 11pt;
            }
            QFrame {
                background-color: #34495e;
                border: 1px solid #2c3e50;
                border-radius: 8px;
            }
            QLabel {
                background-color: transparent;
                border: none;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4ea8e1;
            }
            QPushButton:pressed {
                background-color: #2980b9;
            }
            QPushButton#g_mode {
                background-color: #e74c3c;
            }
            QPushButton#g_mode:hover {
                background-color: #f16a5c;
            }
            QPushButton#g_mode:pressed {
                background-color: #c0392b;
            }
        """)

    def update_stats(self):
        """Fetches and updates the system statistics."""
        # --- CPU Temperature ---
        try:
            temps = psutil.sensors_temperatures()
            if 'coretemp' in temps:
                cpu_temps = [temp.current for temp in temps['coretemp']]
                avg_temp = sum(cpu_temps) / len(cpu_temps)
                self.cpu_temp_value.setText(f"{avg_temp:.1f} °C")
            else:
                self.cpu_temp_value.setText("N/A")
        except (AttributeError, KeyError):
            self.cpu_temp_value.setText("Error")

        # --- RAM Usage ---
        try:
            ram = psutil.virtual_memory()
            self.ram_usage_value.setText(f"{ram.percent}% ({ram.used/1024**3:.1f}/{ram.total/1024**3:.1f} GB)")
        except Exception:
            self.ram_usage_value.setText("Error")

        # --- Fan Speeds ---
        try:
            fans = psutil.sensors_fans()
            if 'dell_smm' in fans and len(fans['dell_smm']) >= 2:
                self.fan1_speed_value.setText(f"{fans['dell_smm'][0].current} RPM")
                self.fan2_speed_value.setText(f"{fans['dell_smm'][1].current} RPM")
            else:
                self.fan1_speed_value.setText("N/A")
                self.fan2_speed_value.setText("N/A")
        except (AttributeError, KeyError):
            self.fan1_speed_value.setText("Error")
            self.fan2_speed_value.setText("Error")
            
        # --- Battery Health ---
        try:
            # Paths for battery capacity files in Linux sysfs
            # Using energy is more common for modern laptops than charge
            full_design_path = "/sys/class/power_supply/BAT0/energy_full_design"
            current_full_path = "/sys/class/power_supply/BAT0/energy_full"

            # Fallback to charge if energy files don't exist
            if not os.path.exists(full_design_path):
                full_design_path = "/sys/class/power_supply/BAT0/charge_full_design"
                current_full_path = "/sys/class/power_supply/BAT0/charge_full"

            with open(full_design_path, 'r') as f:
                design_capacity = int(f.read().strip())
            
            with open(current_full_path, 'r') as f:
                full_capacity = int(f.read().strip())

            if design_capacity > 0:
                health_percent = (full_capacity / design_capacity) * 100
                self.battery_health_value.setText(f"{health_percent:.1f}%")
            else:
                self.battery_health_value.setText("N/A")

        except (FileNotFoundError, ZeroDivisionError, PermissionError, ValueError):
            self.battery_health_value.setText("N/A")


    def run_cli_command(self, mode):
        """
        Executes the g15-fan-cli.py script with the specified mode.
        Uses pkexec to gain necessary root privileges.
        """
        try:
            command = ['pkexec', 'python3', G15_CLI_SCRIPT_PATH, mode]
            subprocess.Popen(command)
        except FileNotFoundError:
            print(f"Error: Could not find pkexec or python3.")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = G15ControlGUI()
    gui.show()
    sys.exit(app.exec())
