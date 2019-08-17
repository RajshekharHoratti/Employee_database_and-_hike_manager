from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Employees, Departments, DeptEmp, Titles, Salaries
from datetime import datetime, timedelta



COMPANY_STARTED_ON_YEAR = "2015"

TitlesAndSalaries = [
    {
        "title": "STAFF",
        "salary": 300000
    },
    {
        "title": "SENIOR STAFF",
        "salary": 500000
    },
    {
        "title": "ASSISTANT ENGINEER",
        "salary": 700000
    },
    {
        "title": "ENGINEER",
        "salary": 700000
    },
    {
        "title": "SENIOR ENGINEER",
        "salary": 1200000
    },
    {
        "title": "TECHNIQUE LEAD",
        "salary": 2000000
    },
    {
        "title": "MANGER",
        "salary": 3000000
    },
]


class EmployeeHire(APIView):
    def post(self, request):
        success_employees = []
        for employee in request.data['employeeDetails']:
            check_employee = Employees.objects.filter(emp_no=employee['employee_id'])
            if check_employee.count() > 0:
                print("Employee Exists")
            else:
                for title in TitlesAndSalaries:
                    if title['title'] == employee['title'].upper():
                        if title['salary'] == employee['salary']['salary_to_date']:
                            birth_date = datetime.strptime(employee['birth_date'], '%Y-%m-%d').date()
                            hire_date = datetime.strptime(employee['hire_date'], '%Y-%m-%d').date()
                            from_date = datetime.strptime(employee['salary']['from_date'], '%Y-%m-%d').date()
                            today_date = datetime.now().date()
                            employee_age = (today_date - birth_date) // timedelta(days=365.2425)

                            hire_year = hire_date.year

                            if str(hire_year) == COMPANY_STARTED_ON_YEAR:
                                if employee_age >= 18 and employee_age < 60:

                                    add_employee = Employees(emp_no=employee['employee_id'], birth_date=birth_date,
                                                             first_name=employee['first_name'],
                                                             last_name=employee['last_name'], gender=employee['gender'],
                                                             hire_date=hire_date)
                                    add_employee.save()
                                    check_department = Departments.objects.get(dept_no=employee['department'])
                                    add_dept_emp = DeptEmp(emp_no=add_employee, dept_no=check_department, from_date=from_date,
                                                           to_date=today_date)
                                    add_dept_emp.save()

                                    add_salaries = Salaries(emp_no=add_employee, salary=employee['salary']['salary_to_date'],
                                                            from_date=from_date,
                                                            to_date=today_date)
                                    add_salaries.save()

                                    add_title = Titles(emp_no=add_employee,
                                                       title=employee['title'],
                                                       from_date=from_date,
                                                       to_date=today_date)
                                    add_title.save()
                                    success_employees.append(employee['employee_id'])
                                else:
                                    print("Invalid Age")
                            else:
                                print("Invalid Hire Year")
                        else:
                            print("Invalid Salary")
                    else:
                        print("Invalid Title")

        response_message = {
            "message": "Success",
            "success_employees": success_employees,
        }

        return JsonResponse(response_message, safe=False, status=200)
