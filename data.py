import os, pandas, random, django


def user():
    from users.models import User
    if not(User.objects.filter()):
        stu_id = [i+j+k for k in [18000000000, 19000000000, 20000000000] for j in [307110000, 307130000, 300180000] for i in range(50)]
        Roads = ["Avenue", "Street", "Road", "Lane"]
        Cities = ["Tokyo", "Delhi", "Manila", "Sao Paulo", "Guangzhou", "Shanghai", "Beijing", "Los Angeles", "Bangkok",
                  "Seoul", "Buenos Aires", "Paris", "London", "Madrid", "Hong Kong"]
        names = pandas.read_csv(r"playground\names.csv")
        names = list(names['names'])
        user = []
        for stu in stu_id:
            surname = random.choice(names)
            lastname = random.choice(names)
            User.objects.get_or_create(id=stu,
                                name=surname + ' ' + lastname,
                                sex=random.choices(["Male", "Female", "None"], [10, 10, 1], k=1)[0],
                                phone=random.choice(['189', '186', '137', '191', '158']) + str(
                                    random.randint(10000000, 100000000)),
                                email=str(stu) + '@fudan.edu.cn',
                                address=str(random.randint(1, 999)) + ' ' + random.choice(names)[:6] + ' ' +
                                        random.choice(Roads) + ', ' + random.choice(Cities),
                                vip=random.choice([0, 1]))


def publisher():
    from publishers.models import Publishers
    if not (Publishers.objects.filter()):
        Roads = ["Avenue", "Street", "Road", "Lane"]
        Cities = ["Tokyo", "Delhi", "Manila", "Sao Paulo", "Guangzhou", "Shanghai", "Beijing", "Los Angeles", "Bangkok",
                  "Seoul", "Buenos Aires", "Paris", "London", "Madrid", "Hong Kong"]
        Books = pandas.read_csv(r"data\scraping.csv")
        names = pandas.read_csv(r"playground\names.csv")
        names = list(names['names'])
        user = []
        for item in Books['publisher'].drop_duplicates():
            surname = random.choice(names)
            lastname = random.choice(names)
            Publishers.objects.get_or_create(name=item,
                                             phone_number=random.choice(['189', '186', '137', '191', '158']) + str(
                                                 random.randint(10000000, 100000000)),
                                             email=surname + random.choice(
                                                 ['@163.com', '@gmail.com', '@qq.com', '@hotmail.com', '@126.com']),
                                             contacts=surname + ' ' + lastname,
                                             address=str(random.randint(1, 999)) + ' ' + random.choice(names)[:8] + ' ' +
                                                     random.choice(Roads) + ', ' + random.choice(Cities),
                                             )


def writer():
    from writers.models import Writers
    if not (Writers.objects.filter(author_type="Author")):
        Books = pandas.read_csv(r"data\scraping.csv")
        for item in Books['author'].drop_duplicates():
            Writers.objects.get_or_create(name=item,
                                          author_type="Author"
                                          )
    if not (Writers.objects.filter(author_type="Translator")):
        Books = pandas.read_csv(r"data\translators.csv")
        for item in Books['translator'].drop_duplicates():
            Writers.objects.get_or_create(name=item,
                                          author_type="Translator"
                                          )


def classification():
    from books.models import Classification, ClassificationSub
    Books = pandas.read_csv(r"data\scraping.csv")
    if not (Classification.objects.filter()):
        for item in Books['category1'].drop_duplicates():
            Classification.objects.get_or_create(class_name=item)
    if not (ClassificationSub.objects.filter()):
        print("yes")
        for item in Books[['category1', 'category2']].drop_duplicates().itertuples():
            ClassificationSub.objects.get_or_create(class_name=item[2],
                                                    ancestor_class_name=Classification.objects.get(class_name=item[1]))


def book():
    from books.models import Books
    if not (Writers.objects.filter(author_type="Author")):
        Books = pandas.read_csv(r"data\scraping.csv")
        for item in Books['author'].drop_duplicates():
            Writers.objects.get_or_create(name=item,
                                          author_type="Author"
                                          )


def main():
    user()
    publisher()
    writer()
    classification()


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MyBookDB.settings")
    if django.VERSION >= (1, 7):
        django.setup()
    main()
    print("done!")
