import sys
import pexpect


shell = pexpect.spawn('bash', encoding='utf-8')
shell.expect("[#$]")

output = ''

def execute(command):
    shell.sendline(command)
    shell.expect("[#$]")
    print(shell.before.find('whoami'))



if __name__ == '__main__':
    execute('whoami')