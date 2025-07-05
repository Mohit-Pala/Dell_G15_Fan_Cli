

# Dell G15 Fan CLI

A command-line tool and optional GUI to adjust fan speed on Dell G15 series of laptops.

This tool lets you modify the fan status on Dell G15 series of laptops using ACPI commands. G-Mode is a toggle between Game Shift and Balanced mode, as documented in the ArchWiki.

## Tested Models

| Model            | Status               |
|------------------|----------------------|
| G15-5535 (AMD)  | Works-Tested         |
| G15-5525 (AMD)  | Works-Archwiki       |
| G15-5520 (Intel)| Works-Archwiki       |
| G15-5511 (Intel)| Works-Tested         |

**Note for Intel Users:**  
If you encounter issues, you may need to edit `g15-fan-cli.py` with a text editor and replace all instances of `AMW3` with `AMWW`.

## Features

- **Command-Line Interface**: Control fan modes directly from your terminal.
- **Optional GUI Dashboard**: A graphical interface to monitor system stats (CPU Temp, RAM, Fan RPM, Battery Health) and control fan modes with a single click.

<!-- It's recommended to take a screenshot of the GUI and upload it -->

## Requirements

### For Both CLI and GUI
- `acpi_call` or `acpi_call-dkms` kernel module
- Python 3
- `python3-pexpect`
- `pkexec` for root privileges (can be replaced with `sudo` if running from a terminal)
- bash shell

### Additional for GUI
- `python3-pyqt6`
- `python3-psutil`

## Installation of Dependencies

**On Debian/Ubuntu and derivatives:**
```bash
sudo apt update
sudo apt install acpi-call-dkms python3-pexpect python3-pyqt6 python3-psutil
```

**On Arch Linux and derivatives:**
```bash
sudo pacman -Syu acpi_call python-pexpect python-pyqt6 python-psutil
```

## Usage

### 1. Command-Line Interface (CLI)
1. Clone this repository or download the `g15-fan-cli.py` file.
2. Move it to `~/.local/bin` or another directory in your `PATH`.
3. Make it executable: `chmod +x ~/.local/bin/g15-fan-cli.py`
4. Run the following command:
   ```bash
   g15-fan-cli.py <mode>
   ```
   Replace `<mode>` with one of the following options:
   - `b`: Balanced mode
   - `p`: Performance mode
   - `q`: Quiet mode
   - `g`: G-Mode (toggles between Game Shift and Balanced)
   - `h`: Help menu

### 2. Graphical User Interface (GUI)
1. Ensure all dependencies (CLI and GUI) are installed.
2. Place both `g15-fan-cli.py` and `g15-gui.py` in the same directory (e.g., `~/.local/bin`).
3. Make the GUI script executable: `chmod +x ~/.local/bin/g15-gui.py`
4. Launch the GUI by running:
   ```bash
   g15-gui.py
   ```

### Keybinding (Example for Ubuntu/GNOME)
You can bind the GUI or a CLI command to a keyboard shortcut for quick access.

1. Go to `Settings -> Keyboard -> View and Customize Shortcuts -> Custom Shortcuts`.
2. Click `Add Shortcut`.
3. Name: `Dell G15 Control`
4. Command: `/home/your-username/.local/bin/g15-gui.py` (to launch the GUI) OR `/home/your-username/.local/bin/g15-fan-cli.py g` (to toggle G-Mode).
5. Shortcut: Set your desired key combination (e.g., `F9` or `Super+F`).

## References
- The Game Shift ACPI commands were taken from the [ArchWiki page for Dell G15 5525](https://wiki.archlinux.org/title/Dell_G15_5525).
- The rest of the ACPI commands were extracted from the [Dell-G15-Controller GitHub repository](https://github.com/...).
