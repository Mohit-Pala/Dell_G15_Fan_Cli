import pexpect
import sys

tmpShell = pexpect.spawn('bash', encoding='utf-8', logfile=sys.stdout)
tmpShell.expect("[#$]")


def parseAgrs():

    try:
        # Help menu
        if sys.argv[1].lower().startswith('h'):
            printHelp()

        elif sys.argv[1].lower().startswith('p'):
            perfMode()

        elif sys.argv[1].lower().startswith('q'):
            quietMode()

        elif sys.argv[1].lower().startswith('b'):
            balancedMode()

        elif sys.argv[1].lower().startswith('g'):
            GMode()

        elif sys.argv[1].lower().startswith('z'):
            queryGMode()

        else:
            print("invalid usage")
            printHelp()

    # help menu
    except IndexError:
        print('To be used with a system arg, printing help menu')
        printHelp()

# Fan modes


def perfMode():
    # Performance mode
    # "\_SB.AMW3.WMAX 0 0x15 {0x01, 0xa1, 0x00, 0x00}"
    prelimChecks()
    notify_send('Activating performance mode')
    executeAcpiCall('echo "\\_SB.AMW3.WMAX 0 0x15 {1, 0xa1, 0x00, 0x00}" > /proc/acpi/call')


def balancedMode():
    # Balanced mode
    # "\_SB.AMW3.WMAX 0 0x15 {0x01, 0xa0, 0x00, 0x00}"
    prelimChecks()
    notify_send('Activating balanced mode')
    executeAcpiCall('echo "\\_SB.AMW3.WMAX 0 0x15 {1, 0xa0, 0x00, 0x00}" > /proc/acpi/call')


def quietMode():
    # Quiet mode
    # "\_SB.AMW3.WMAX 0 0x15 {0x01, 0xa3, 0x00, 0x00}"
    prelimChecks()
    notify_send('Activating quiet mode')
    executeAcpiCall('echo "\\_SB.AMW3.WMAX 0 0x15 {1, 0xa3, 0x00, 0x00}" > /proc/acpi/call')


def GMode():
    # Gmode
    # "\_SB.AMW3.WMAX 0 0x15 {1, 0xab, 0x00, 0x00}"
    # "\_SB.AMW3.WMAX 0 0x25 {1, 0x01, 0x00, 0x00}"
    if (queryGMode()):
        notify_send('Deactivating GMode\nActivating balanced mode')
        executeAcpiCall('echo "\\_SB.AMW3.WMAX 0 0x15 {1, 0xa0, 0x00, 0x00}" > /proc/acpi/call')
        executeAcpiCall('echo "\\_SB.AMW3.WMAX 0 0x25 {1, 0x00, 0x00, 0x00}" > /proc/acpi/call')
    else:
        executeAcpiCall('echo "\\_SB.AMW3.WMAX 0 0x15 {1, 0xab, 0x00, 0x00}" > /proc/acpi/call')
        executeAcpiCall('echo "\\_SB.AMW3.WMAX 0 0x25 {1, 0x01, 0x00, 0x00}" > /proc/acpi/call')
        notify_send('Activating GMode')


def queryGMode():
    # "\_SB.AMW3.WMAX 0 0x14 {0x0b, 0x00, 0x00, 0x00}"
    # 0xab is on, else off
    prelimChecks()
    executeAcpiCall(
        'echo "\\_SB.AMW3.WMAX 0 0x14 {0x0b, 0x00, 0x00, 0x00}" > /proc/acpi/call; cat /proc/acpi/call')
    if tmpShell.before.find('0xab') > 0:
        # fan on
        notify_send('Fan On')
        return True
    else:
        # fan off
        notify_send('Fan Off')
        return False


# check if acpi call is loaded
def prelimChecks():
    elevate()
    executeAcpiCall('lsmod | grep -i acpi_call')
    if tmpShell.before.find('acpi_call') > 0:
        pass
    else:
        notify_send('Acpi Call module not loaded')
        exit()

# gain root perms
def elevate():
    tmpShell.sendline('pkexec bash')
    tmpShell.expect("[#$]")

# execute given acpi call
def executeAcpiCall(command):
    tmpShell.sendline(command)
    tmpShell.expect("[#$]")

# send notifs using notify_send
def notify_send(message):
    message = '"' + message + '"'
    notify = pexpect.spawn('bash', encoding='utf-8', logfile=sys.stdout)
    notify.expect("[#$]")
    notify.sendline(str('notify-send -a "Fan Status" -t 5000 ' + message))
    notify.expect("[#$]")
    notify.close()


def printHelp():
    print('Usage:')
    print('python g15-fan-cli.py {{mode}}')
    print('Replace mode with:\nb\tBalanced\np\tPerformance\nq\tQuiet\ng\tGame Shift mode, this is a toggle, will toggle back to balanced if run again\nh\tHelp menu')


if __name__ == '__main__':
    parseAgrs()
