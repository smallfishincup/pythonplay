import re
import time
import requests
 
s = remote('104.197.7.111', 13135)
s.recvuntil("Okay, let's begin with simple questions.\n")
 
problem_number = 1
 
for _ in range(10):
    print ('No. %d --------------------------' % problem_number)
    x = s.recvuntil('Answer (yes/no): ')
    print (x)
    m = re.search('Is (.+) an integer or not?', x)
    expr = m.group(1)
    try:
        ans = str(safeeval.expr(expr))
        print (expr)
        print (ans)
        if ('.' not in ans) or re.search(r'\.0+$', ans):
            s.send('yes\n')
        else:
            s.send('no\n')
    except:
        s.send('no\n')
    problem_number += 1
 
print (s.recvuntil('Time for calculating weird integer sequences.'))
 
for i in range(35):
    print ('No. %d --------------------------' % problem_number)
    s.recvuntil('Description: ')
    desc = s.recvuntil('\n')[:-1]
 
    buf = s.recv(1)
    seq = None
    if 'T' in buf:
        s.recvuntil('starts with: ')
        seq = s.recvuntil('\n')[:-1]
 
    print ('Description:', desc)
    print ('The sequence starts with:', seq)
    search = 'name:"%s"' % desc
    if seq and len(seq) < 40:
        search += ' seq:"%s"' % seq
 
    print ('Searching %s' % search)
    res = requests.get('http://oeis.org/search', params={'q': search})
 
    m = re.search('<a href="/A([0-9]+)"', res.text)
    num = m.group(1)
    print ('found page:', num)
 
    res = s.recvuntil('Answer: ')
    m = re.search(r' = (\d+), ', res)
    n = int(m.group(1))
    print ('n = ', n)
 
    res = requests.get('http://oeis.org/A%s/b%s.txt' % (num, num))
    m = re.search('^%d +(-?[0-9]+)' % n, res.text, re.MULTILINE)
    if m is None:
        print ('not found')
        ans = raw_input('Input answer: ')
    else:
        ans = int(m.group(1))
    print ('Answer =', ans)
    s.send(str(ans) + '\n')
    problem_number += 1
    time.sleep(0.2)
 
 
print ('No. %d --------------------------' % problem_number)
s.recvuntil('Description: ')
desc = '"' + s.recvuntil('\n')[:-1] + '"'
s.recvuntil('The sequence starts with: ')
seq = s.recvuntil('\n')
res = s.recvuntil('Answer: ')
m = re.search(r'n = (\d+), ', res)
n = int(m.group(1))
print ('n = ', n)
ans = raw_input('Input answer: ')
print ('Answer =', ans)
s.send('%s\n' % ans)
problem_number += 1
 
print ('No. %d --------------------------' % problem_number)
s.recvuntil('Description: ')
desc = '"' + s.recvuntil('\n')[:-1] + '"'
s.recvuntil('The sequence starts with: ')
seq = s.recvuntil('\n')
res = s.recvuntil('Answer: ')
m = re.search(r'n = (\d+), ', res)
n = int(m.group(1))
ans = sympy.binomial(2*n, n)/(n+1)
print ('Answer =', ans)
s.send('%d\n' % ans)
problem_number += 1
 
s.interactive()