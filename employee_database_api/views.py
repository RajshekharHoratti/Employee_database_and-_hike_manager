from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Employees, Departments, DeptEmp, Titles, Salaries
from datetime import datetime, timedelta



COMPANY_STARTED_ON_YEAR = "2015"


DEPARTMENTS_ELIGIBLE_FOR_HIKE = ["Customer Service", "Development", "Finance", "Human Resources", "Sales"]
TITLES_ELIGIBLE_FOR_HIKE = ["Senior Engineer", "Staff", "Engineer", "Senior Staff", "Assistant Engineer", "Technique Leader"]

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

            try:
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
                                current_date = datetime.now().date()
                                employee_age = (current_date - birth_date) // timedelta(days=365.2425)

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
                                                               to_date=current_date)
                                        add_dept_emp.save()

                                        add_salaries = Salaries(emp_no=add_employee, salary=employee['salary']['salary_to_date'],
                                                                from_date=from_date,
                                                                to_date=current_date)
                                        add_salaries.save()

                                        add_title = Titles(emp_no=add_employee,
                                                           title=employee['title'],
                                                           from_date=from_date,
                                                           to_date=current_date)
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
            except:
                print("Some Internal Server Error")

        response_message = {
            "message": "Success",
            "success_employees": success_employees,
        }
        return JsonResponse(response_message, safe=False, status=200)


class EmployeeEligibleForHike(APIView):
    def get(self, request):
        try:
            employee_id = request.GET.get('employee_id')
            employeeDetails = Employees.objects.get(emp_no=employee_id)
            if employeeDetails:
                deptEmpDetails = DeptEmp.objects.get(emp_no=employeeDetails).dept_no
                if deptEmpDetails:
                    deptDetails = Departments.objects.all()
                    if deptDetails.count() > 0:
                        for empDept in deptDetails:
                            if deptEmpDetails.dept_no == empDept.dept_no:
                                titleDetails = Titles.objects.get(emp_no=employeeDetails)

                                print(deptEmpDetails.dept_no)
                                print(empDept.dept_no)
                                print(titleDetails.title)

                                if empDept.dept_name in DEPARTMENTS_ELIGIBLE_FOR_HIKE and titleDetails.title in TITLES_ELIGIBLE_FOR_HIKE:
                                    birth_date = employeeDetails.birth_date
                                    current_date = datetime.now().date()
                                    experience = (current_date - employeeDetails.hire_date) // timedelta(days=365.2425)
                                    employee_age = (current_date - birth_date) // timedelta(days=365.2425)
                                    if experience <= 1 or employee_age <= 20:
                                        response_message = {
                                            "message": "Experience or Employee age Condition Failed",
                                            "hike": False
                                        }
                                        return JsonResponse(response_message, safe=False, status=200)
                                    else:
                                        if employeeDetails.gender == "M" and titleDetails.title == "Technique Leader":
                                            response_message = {
                                                "message": "Gender or Title Condition Failed",
                                                "hike": False
                                            }
                                            return JsonResponse(response_message, safe=False, status=200)
                                        else:

                                            for item in range(len(TitlesAndSalaries)):
                                                if titleDetails.title.upper() == TitlesAndSalaries[item]['title']:
                                                    if (item + 1) < len(TitlesAndSalaries):
                                                        response_message = {
                                                            "message": "Success",
                                                            "hike": True,
                                                            "designation": TitlesAndSalaries[item + 1]['title']
                                                        }
                                                        return JsonResponse(response_message, safe=False, status=200)
                                                    else:
                                                        response_message = {
                                                            "message": "Success, But this is the last title avaliable",
                                                            "hike": True,
                                                            "designation": TitlesAndSalaries[item]['title']
                                                        }
                                                        return JsonResponse(response_message, safe=False, status=200)
                                                else:
                                                    pass
                                else:
                                    response_message = {
                                        "message": "Not Eligible for Hike..!!",
                                        "hike": False
                                    }
                                    return JsonResponse(response_message, safe=False, status=200)
                            else:
                                pass

                    else:
                        response_message = {
                            "message": "Invalid Department..!!",
                            "hike": False
                        }
                        return JsonResponse(response_message, safe=False, status=200)
                else:
                    response_message = {
                        "message": "Invalid Department..!!",
                        "hike": False
                    }
                    return JsonResponse(response_message, safe=False, status=200)
            else:
                response_message = {
                    "message": "Invalid Employee..!!",
                    "hike": False
                }
                return JsonResponse(response_message, safe=False, status=200)
        except:
            response_message = {
                "hike": False
            }
            return JsonResponse(response_message, safe=False, status=200)



