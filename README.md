# Employee_database_and_hike_manager

This is a Demo of a Employee Database and a Employee hike Manager with some conditions.

Requirements:

1. PostgreSQL
2. Python 3.*

and Install all the requirements from the requirements.txt file by using the below command.
      pip install -r requirements.txt 


Database tables:

#1 employees
#2 departments
#3 dept_emp
#4 titles
and
#5 salaries


The departments table should contain Data:
'd009', 'Customer Service'
'd005', 'Development'
'd002', 'Finance'
'd003', 'Human Resources'
'd001', 'Marketing'
'd004', 'Production'
'd006', 'Quality Management'
'd008', 'Research'
'd007', 'Sales'

DATABASE SETUP:
Go to Settings.py


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'DATABASE_NAME',
        'USER': 'DATABASE_USER_NAME',
        'PASSWORD': 'DATABASE_PASSORD',
        'HOST': 'DATABASE_HOST',
        'PORT': 'DATABASE_PORT',
        }
    }

ex:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'employee_database',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
        }
    }


There are two API's in the project:
1. employee_hire
2. eligible_for_hike


Assumptions:
1. Consider company started in 2015


1. employee_hire
METHOD: POST
BODY: {
    "employeeDetails": [
        {
            "birth_date": "1993-06-25",
            "employee_id": 1,
            "first_name": "xxx",
            "last_name": "yyy",
            "gender": "M",
            "hire_date": "2018-06-01",
            "department": "d005",
            "title": "Engineer",
            "salary": 900000,
            "salaryDates": {
                "from_date": "2018-04-11",
                "to_date": "2019-08-17"
            }
        }
    ]
}

Using this API you can add a employee into your database and there are some conditions that need to be satisfied inorder to add a empolyee
1.The employee age must be in the range of 18 to 60
2.Each employee should be hired in one of the departments above.
3.Title hierarchy is as follows (first being lowest and last being thehighest)
          a. Staff,
          b. Senior staff,
          c. Assistant Engineer
          d. Engineer,
          e. Senior Engineer
          f. Technique Lead
          g. Manger
 Salaries according to title:
          0. Staff : 3L
          1. Senior staff: 5L
          2. Assistant Engineer: 7L
          3. Engineer: 9L
          4. Senior Engineer: 12L
          5. Technique Lead: 20L
          6. Manger: 30L


2.eligible_for_hike
METHOD: GET
PARAMETERS:employee_id
ex: http://localhost:8000/eligible_for_hike/?employee_id=1

Using this API you can get if the employee Id specified is elegible for a Hike or not is yes then what is the title he will be promoted to.
conditions to get a hike:
1.Department not in [“Customer Service”, “Development”, “Finance”, “Human Resources”, “Human Resources”,
“Sales”] OR Title not in [“Senior Engineer”, “Staff”, “Engineer”, “Senior Staff”, “Assistant Engineer”, “Technique
Leader”] if True then No Hike else Hike

2. Experience <= 1 year OR age <= 20 if True then No Hike else Hike
3.Gender = M AND title = Technique Leader If True then No Hike else Hike.

