import pandas
import random

stu_id = [i+j+k for k in [18000000000, 19000000000, 20000000000] for j in [307110000, 307130000, 300180000] for i in range(500)]
print(stu_id)
names = pandas.read_csv(r"C:\Users\Daniel\Desktop\数据库\MyBookDB\playground\names.csv")
names = list(names['names'])
user = []
for stu in stu_id:
    surname = random.choice(names)
    lastname = random.choice(names)
    user.append([surname + ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=2)),
         surname + ' ' + lastname,
         random.choices(["Male", "Female", "None"], [10, 10, 1], k=1)[0],
         random.choice(['189', '186', '137', '191', '158']) + str(random.randint(10000000, 100000000)),
         str(stu) + '@fudan.edu.cn',
         surname[0] + lastname[0] + str(random.randint(2000, 2002)) + '%0.2d' % (random.randint(1, 13)) + '%0.2d' % (random.randint(1, 29)),
         random.choice([0, 1])])
user = pandas.DataFrame(user, columns=['username', 'name', 'sex', 'phone', 'email', 'pwd', 'vip'])
print(user)
user.to_csv(r'C:\Users\Daniel\Desktop\数据库\MyBookDB\playground\users.csv')