# python-flask-noteapp
This application helps to add notes which is essential in our daily life. Application has developed with Python-Flask, BootStrap and its database is MySQL

## Pre-requisite
* Python should be installed
* Install the below packages using pip

    ```pip install flask```
    ```pip install flask_bootstrap```
    ```pip install requests```
    ```pip install flask_mysqldb```

## Datbase changes
* Create a MySQL DB.
* Require two tables, ```user``` for stroring the user details. ```todo``` for storing the todos created by the user.
* Create the ```user``` table by executing below query

    ```CREATE TABLE user(user_id int auto_increment, first_name varchar(20), last_name varchar(20), username varchar(20) unique, email varchar(30) unique, password varchar(100), primary key(user_id));```
* Create the ```todo``` table by executing below query

    ```CREATE TABLE todo(todo_id int auto_increment, user_id int, title varchar(100), body varchar(1000), primary key(todo_id));```
* Make sure the DB connection details are properly updated in ```flask_app.py``` file.

## Checkout & Build
```
* `git clone` https://github.com/vishnuar/python-flask-noteapp.git
* `cd` python-flask-noteapp
```

## Run the apps
```shell
python flask_app.py
```

## Note
Application has hosted in pythonanywhere and its url is https://vishnuar.pythonanywhere.com/noteapp

### Login screen
![image](https://user-images.githubusercontent.com/37209530/95227992-66b24e00-081c-11eb-9a95-0585350cc3f3.png)

### User registration screen
![image](https://user-images.githubusercontent.com/37209530/95228148-982b1980-081c-11eb-8c5a-88c76c1e04ab.png)

### Home screen
![image](https://user-images.githubusercontent.com/37209530/95228372-dd4f4b80-081c-11eb-8ec5-c4e3e5d9f5c4.png)

## Author
* Vishnu A R