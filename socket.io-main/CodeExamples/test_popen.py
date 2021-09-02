# 3 easy methods for running command in python

from subprocess import run, PIPE, Popen, check_output

# mwthod 1 ★
p = Popen(['date', '-R'], stdout=PIPE)
print(p.communicate()[0].decode())

# mwthod 2 ★★
out = run(['date', '-R'], stdout=PIPE)
print(out.stdout.decode())

# mwthod 3 ★★★
print(check_output(['date', '-R']).decode())