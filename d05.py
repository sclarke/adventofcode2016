from hashlib import md5

door_id = b'cxdnnyjw'


# password = []
# i = 0
# while len(password) < 8:
#     dig = md5(door_id + '{:d}'.format(i).encode()).hexdigest()
#     if dig.startswith('00000'):
#         password.append(dig[5])
#         print(dig[5], end='')
#     i += 1
#
# print()

def xstr(s):
    return ' ' if s is None else str(s)


password = [None] * 8
i = 0
while None in password:
    dig = md5(door_id + '{:d}'.format(i).encode()).hexdigest()
    if dig.startswith('00000') and int(dig[5], base=16) < 8 and password[int(dig[5])] is None:
        password[int(dig[5])] = dig[6]
        print(''.join(xstr(s) for s in password))
    i += 1

print(i)
