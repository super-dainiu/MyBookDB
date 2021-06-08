import pandas
import random

stu_id = [i+j+k for k in [18000000000, 19000000000, 20000000000] for j in [307110000, 307130000, 300180000] for i in range(500)]
Roads = ["Avenue", "Street", "Road", "Lane"]
Cities = ["Tokyo", "Delhi", "Manila", "Sao Paulo", "Guangzhou", "Shanghai", "Beijing", "Los Angeles", "Bangkok",
          "Seoul", "Buenos Aires", "Paris", "London", "Madrid", "Hong Kong"]
Publishers = [" Books", " Press", " House", "'s"]
names = pandas.read_csv(r"..\playground\names.csv")
names = list(names['names'])
user = []
for stu in stu_id:
    surname = random.choice(names)
    lastname = random.choice(names)
    companyname = random.choice(names)
    user.append([companyname + random.choice(Publishers),
                 random.choice(['189', '186', '137', '191', '158']) + str(random.randint(10000000, 100000000)),
                 str(stu) + '@sjtu.edu.cn',
                 surname + ' ' + lastname,
                 str(random.randint(1, 999)) + ' ' + random.choice(names)[:8] + ' ' + random.choice(
                     Roads) + ', ' + random.choice(
                     Cities),
                 ])
user = pandas.DataFrame(user, columns=['name', 'phone_number', 'email', 'contacts', 'address'])
print(user)
user.to_csv(r'..\data\publishers.csv')