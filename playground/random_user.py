import pandas
import random

stu_id = [i+j+k for k in [18000000000, 19000000000, 20000000000] for j in [307110000, 307130000, 300180000] for i in range(500)]
Roads = ["Avenue", "Street", "Road", "Lane"]
Cities = ["Tokyo", "Delhi", "Manila", "Sao Paulo", "Guangzhou", "Shanghai", "Beijing", "Los Angeles", "Bangkok",
          "Seoul", "Buenos Aires", "Paris", "London", "Madrid", "Hong Kong"]
names = pandas.read_csv(r"..\playground\names.csv")
names = list(names['names'])
user = []
for stu in stu_id:
    surname = random.choice(names)
    lastname = random.choice(names)
    user.append(
        [surname + ' ' + lastname,
         random.choices(["Male", "Female", "None"], [10, 10, 1], k=1)[0],
         random.choice(['189', '186', '137', '191', '158']) + str(random.randint(10000000, 100000000)),
         str(stu) + '@fudan.edu.cn',
         str(random.randint(1, 999)) + ' ' + random.choice(names)[:6] + ' ' + random.choice(Roads) + ', ' + random.choice(
             Cities),
         random.choice([0, 1])])
user = pandas.DataFrame(user, columns=['name', 'sex', 'phone', 'email', 'address', 'vip'])
print(user)
user.to_csv(r'..\data\users.csv')
