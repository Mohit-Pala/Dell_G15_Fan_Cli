import sys
import pexpect

if __name__ == '__main__':
    shell = pexpect.spawn('bash', encoding='utf-8', logfile=sys.stdout)
    shell.expect("[#$]")
    shell.sendline('whoami')
    shell.expect("[#$]")