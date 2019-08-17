from django.db import models


# Create your models here.


class MyGenderChoices:
    M = "M"
    F = "F"

    GENDER_ENUM_CHOICES = (
        (0, 'M'),
        (0, 'F')
    )


class Employees(models.Model):
    emp_no = models.IntegerField(default=0, null=False, primary_key=True)
    birth_date = models.DateField(null=False)
    first_name = models.CharField(max_length=14, null=False)
    last_name = models.CharField(max_length=16, null=False)
    gender = models.CharField(choices=MyGenderChoices.GENDER_ENUM_CHOICES, max_length=1, null=False)
    hire_date = models.DateField(null=False)


class Departments(models.Model):
    dept_no = models.CharField(max_length=4, primary_key=True)
    dept_name = models.CharField(max_length=40, unique=True)


class DeptEmp(models.Model):
    emp_no = models.ForeignKey(Employees, null=False, on_delete=models.CASCADE)
    dept_no = models.ForeignKey(Departments, on_delete=models.CASCADE)
    from_date = models.DateField(null=False)
    to_date = models.DateField(null=False)


class Titles(models.Model):
    emp_no = models.ForeignKey(Employees, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False)
    from_date = models.DateField(null=False, primary_key=True)
    to_date = models.DateField(null=False)


class Salaries(models.Model):
    emp_no = models.ForeignKey(Employees, null=False, on_delete=models.CASCADE)
    salary = models.IntegerField(null=False)
    from_date = models.DateField(null=False, primary_key=True)
    to_date = models.DateField(null=False)
