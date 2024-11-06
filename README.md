# Dell G15 fan cli
## A command-line tool to adjust fan speed on Dell G15 series of laptops

This tool lets you modify the fan status on Dell G15 series of laptops using ACPI commands.

G-Mode is a toggle between Game shift and Balanced mode, that's how it is in the archwiki

Curretnly tested on the following models:

|  Model             |  Status            |
|--------------------|--------------------|
|  G15-5535 (AMD)    |  Works-Tested      |
|  G15-5530 (Intel)  |  Works-Tested      |
|  G15-5525 (AMD)    |  Works-Archwiki    |
|  G15-5520 (Intel)  |  Works-Archwiki    |
|  G15-5511 (Intel)  |  Works-Tested      |


# Intel users:
Use a text editor to find a replace

Find -> `AMW3`

Replace with -> `AMWW`

# Requirements:
- ACPI_CALL or ACPI_CALL-DKMS kernel module 
- python
- python-pexpect
- bash shell
- pkexec: root privileges, can replace with sudo if running from a terminal

# Usage
1. Git clone this repo or download the python file
2. Move it to `~/.local/bin` or any directory
3. Run the following command: `python ~/.local/bin/g15-fan-cli.py <mode>`

Replace `<mode>` with one of the following options:
- `b  `       Balanced mode
- `p  `       Performance mode
- `q  `       Quiet mode
- `g  `       G-Mode, switch between balanced and Game Shift mode
- `h  `       Help menu

# Bind to F9 key
## On KDE Desktop
1. Go to System settings -> workspaces -> shortcuts -> add command
2. Type `konsole -e python ~/.local/bin/g15-fan-cli.py g`
3. Select the newly created command -> add custom shortcut -> bind to f9 -> apply

# References
- The Game shift ACPI commands were taken from the Archwiki page for Dell g15-5525: https://wiki.archlinux.org/title/Dell_G15_5525
- Used Dell-G15-Controller GitHub repository to extract the rest of the ACPI commands: https://github.com/cemkaya-mpi/Dell-G15-Controller
