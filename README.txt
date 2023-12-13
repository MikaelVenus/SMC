1)Clone this project to a directory
2)Create the virtual environment
 -Go to project folder
 -run python [-m venv smcvenv]
3)Activate virtual env
 -in project diectory
 -[cd smcvenv]
 -[cd Scripts]
 -[activate]

4) Install package
 -back to project directory smcproject
 -[pip install django]
 -[pip install pymysql]
 -make sure you install mysql and set database config in setting.py
5) Do database migration
 -python manage.py makemigrations
 -python manage.py migrate

6) Runserver (in smcproject dir)
 -[python manage.py runserver]

7) Create Super User 
 -[python manage.py createsuperuser]