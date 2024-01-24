import pexpect
import sys

def parseAgrs():

    try:
        # Help menu
        if sys.argv[1].lower().startswith('h'):
            printHelp()
        
        # Performance mode
        # "\_SB.AMW3.WMAX 0 0x15 {0x01, 0xa1, 0x00, 0x00}"
        if sys.argv[1].lower().startswith('p'):
            perfMode()

        # Quiet mode
        # "\_SB.AMW3.WMAX 0 0x15 {0x01, 0xa3, 0x00, 0x00}"
        if sys.argv[1].lower().startswith('q'):
            quietMode()

        # Balanced mode
        # "\_SB.AMW3.WMAX 0 0x15 {0x01, 0xa0, 0x00, 0x00}"
        if sys.argv[1].lower().startswith('b'):
            balancedMode()

        # Gmode
        # "\_SB.AMW3.WMAX 0 0x15 {1, 0xab, 0x00, 0x00}"
        # "\_SB.AMW3.WMAX 0 0x25 {1, 0x01, 0x00, 0x00}" 
        if sys.argv[1].lower().startswith('g'):
            GMode()

    # help menu
    except IndexError:
        print('To be used with a system arg, printing help menu')
        printHelp()
    
# Fan modes
def perfMode():
    notify_send('Activating performance mode')
    

def balancedMode():
    pass

def quietMode():
    pass

def GMode():
    pass 

def executeAcpiCall(command):
    tmpShell = pexpect.spawn('pkexec bash', encoding='utf-8', logfile=sys.stdout)
    tmpShell.expect("[#$]")
    tmpShell.sendline(command)
    tmpShell.expect("[#$]")

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