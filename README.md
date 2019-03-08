Django REST Vue project template
================================



How to install
--------------

$ django-admin.py startproject \
  --template=https://github.com/enqack/django-rest-vue-project-template/archive/master.zip \
  --extension=py,md,env \
  project_name
$ cd project_name
$ mv example.env .env
$ mv example.logging.yaml logging.yaml
$ pipenv install -dev
$ pipenv shell
$ python3 manage.py migrate
$ python3 manage.py loaddata assets/fixtures/*
$ python3 manage.py createsuperuser
$ python3 manage.py runserver_plus 0.0.0.0:8000
