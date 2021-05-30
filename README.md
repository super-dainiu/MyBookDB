# MyBookDB
Project for 数据库及实现
# Installation
1. Create virtualenv and install dependencies:

  ```
  pip install -r requirements.txt
  ```
2. Set up database and replace my username and password in project root file "MyBookDB/settings.py" containing something like:

  ```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "MyBookDB",
        'USER': username,
        'PASSWORD': password,
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}
  ```
3. Apply migrations and create superuser:
  
  ```
  python manage.py migrate --fake
  python manage.py createsuperuser
  ```
