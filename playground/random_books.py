import pandas
import random

basics = ["Beginner's Guides for %s", "A Computer Programmer's View of %s", "Introduction to %s", "Head First %s"]
advanced = ["Effective %s", "Advanced Tutorial for %s", "%s Development", "All of %s", "%s with Applications"]
specialized_for = ["%s Tutorial for %s", "Effective %s for %s", "%s-%s"]
specialized_with = ["%s with %s", "%s in %s"]
languages = ["Python", "Java", "C", "C++", "C#", "Ruby", "PHP", "HTML", "MySQL", "LateX", "Fortran", "Matlab", "Go",
             "Pascal", "JavaScript", "Linux", "R", "Github"]
fields = ["Machine Learning", "Numerical Algorithms", "Data Science", "Web Development", "Software Engineering",
          "Deep Learning", "Databases", "Artificial Intelligence", "Game Designs", "Computer Architecture",
          "Social Network Mining", "Statistics", "Operating Systems", "Algorithms",
          ]
f = pandas.read_csv(r"C:\Users\Daniel\Desktop\数据库\MyBookDB\playground\names.csv")
names = list(f['names'])
person = [random.choice(names)+' '+random.choice(names) for i in range(5000)]
authors = random.choices(person, k=200)
translators = random.choices(person, k=200)
books = []

for i in range(100000):
    x = random.randint(1, 5)
    if x == 1:
        y = random.randint(1, 2)
        if y == 1:
            field = "Basics"
            pattern = random.choice(basics)
        else:
            field = "Advanced"
            pattern = random.choice(advanced)
        language = random.choice(languages)
        name = pattern % language
    elif x == 2:
        y = random.randint(1, 2)
        if y == 1:
            pattern = random.choice(basics)
        else:
            pattern = random.choice(advanced)
        language = "None"
        field = random.choice(fields)
        name = pattern % field
    else:
        y = random.randint(1, 2)
        language = random.choice(languages)
        field = random.choice(fields)
        if y == 1:
            pattern = random.choice(specialized_for)
            name = pattern % (language, field)
        else:
            pattern = random.choice(specialized_with)
            name = pattern % (field, language)
    books.append((name, field, language))
books = list(set(books))
info = []
for item in books:
    info.append([*item,random.choice(authors), random.choice(translators)])
for item in info:
    print(item)