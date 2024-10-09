'''
Credits to whatever website I took this from
'''

def hanoi(n, f, to, via):
    if n == 1:
        print("Move disk 1 from",f,"to",to)
    else:
        hanoi(n-1, f, via, to)
        print("Move disk",n,"from",f,"to",to)
        hanoi(n-1, via, to, f)


n = 3
f = 'A'
to = 'B'
via = 'C'
hanoi(n, f, via, to)