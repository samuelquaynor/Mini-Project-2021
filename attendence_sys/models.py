from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from django.contrib.auth.models import PermissionsMixin, User
from django.utils.translation import gettext_lazy as _



def user_directory_path(instance, filename): 
    name, ext = filename.split(".")
    name = instance.firstname + instance.lastname
    filename = name +'.'+ ext 
    return 'Faculty_Images/{}'.format(filename)

# class Faculty(models.Model):

#     user = models.OneToOneField(User, null = True, blank = True, on_delete= models.CASCADE)
#     firstname = models.CharField(max_length=200, null=True, blank=True)
#     lastname = models.CharField(max_length=200, null=True, blank=True)
#     phone = models.CharField(max_length=200, null=True)
#     email = models.CharField(max_length=200, null=True)
#     profile_pic = models.ImageField(upload_to=user_directory_path ,null=True, blank=True)

#     def __str__(self):
#         return str(self.firstname + " " + self.lastname)


def student_directory_path(instance, filename): 
    name, ext = filename.split(".")
    name = instance.registration_id # + "_" + instance.branch + "_" + instance.year + "_" + instance.section
    filename = name +'.'+ ext 
    return 'Student_Images/{}/{}/{}/{}'.format(instance.course,instance.year,instance.faculty,filename)

def teacher_directory_path(instance, filename): 
    name, ext = filename.split(".")
    name = instance.registration_id # + "_" + instance.branch + "_" + instance.year + "_" + instance.section
    filename = name +'.'+ ext 
    return 'Teacher_Images/{}/{}'.format(instance.course,filename)

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, firstname, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, firstname, password, **other_fields)

    def create_user(self, email, username, firstname, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          firstname=firstname, **other_fields)
        user.set_password(password)
        user.save()
        return user

class Teacher(AbstractBaseUser, PermissionsMixin, models.Model):

    Faculty = (
        ('Select Faculty','Select Faculty'),
        ('Faculty of Agriculture','Faculty of Agriculture'),
        ('Faculty of Renewable Natural Resources','Faculty of Renewable Natural Resources'),
        ('Faculty of Built Environment','Faculty of Built Environment'),
    )
    Department = (
        ('Select Department','Select Department'),
        ('Department of Agricultural Economics','Department of Agricultural Economics'),
        ('Department of Animal Science','Department of Animal Science'),
        ('Department of Horticulture','Department of Horticulture'),
    )
    Course = (
        ('Select Course','Select Course'),
        ('BSc Agriculture (Economics Option)','BSc Agriculture (Economics Option)'),
        ('BSc Agriculture (Extension Option)','BSc Agriculture (Extension Option)'),
        ('BSc Agribusiness Management','BSc Agribusiness Management'),
    )
    GENDER = (
        ('MALE','MALE'),
        ('FEMALE','FEMALE'),
    )

    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    firstname = models.CharField(max_length=200, null=True)
    lastname = models.CharField(max_length=200, null=True, blank=True)
    registration_id = models.CharField(max_length=200, null=True)
    faculty = models.CharField(max_length=100, null=True, choices=Faculty)
    department = models.CharField(max_length=100, null=True, choices=Department)
    course = models.CharField(max_length=100, null=True, choices=Course)
    gender = models.CharField(max_length=100, null=True, choices=GENDER)
    date = models.DateField(auto_now_add = True, null = True)
    profile_pic = models.ImageField(upload_to=teacher_directory_path ,null=True, blank=True)
    about = models.TextField(_('about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'firstname', 'lastname', 'registration_id', 'faculty', 'department', 'course', 'gender']

    class Meta:
        verbose_name_plural = "Teachers" 

    def __str__(self):
        return str(self.username)

class Student(models.Model):

    Faculty = (
        ('Select Faculty','Select Faculty'),
        ('Faculty of Agriculture','Faculty of Agriculture'),
        ('Faculty of Renewable Natural Resources','Faculty of Renewable Natural Resources'),
        ('Faculty of Built Environment','Faculty of Built Environment'),
    )
    Department = (
        ('Select Department','Select Department'),
        ('Department of Agricultural Economics','Department of Agricultural Economics'),
        ('Department of Animal Science','Department of Animal Science'),
        ('Department of Horticulture','Department of Horticulture'),
    )
    Course = (
        ('Select Course','Select Course'),
        ('BSc Agriculture (Economics Option)','BSc Agriculture (Economics Option)'),
        ('BSc Agriculture (Extension Option)','BSc Agriculture (Extension Option)'),
        ('BSc Agribusiness Management','BSc Agribusiness Management'),
    )
    YEAR = (
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5'),
        ('6','6'),
        ('7','7'),
    )
    GENDER = (
        ('MALE','MALE'),
        ('FEMALE','FEMALE'),
    )

    firstname = models.CharField(max_length=200, null=True, blank=True)
    lastname = models.CharField(max_length=200, null=True, blank=True)
    registration_id = models.CharField(max_length=200, null=True)
    date = models.DateField(auto_now_add = True, null = True)
    course = models.CharField(max_length=100, null=True, choices=Course)
    teacher = models.ForeignKey(Teacher, related_name="students", null=True, on_delete=models.CASCADE)
    year = models.CharField(max_length=100, null=True, choices=YEAR)
    gender = models.CharField(max_length=100, null=True, choices=GENDER)
    faculty = models.CharField(max_length=100, null=True, choices=Faculty)
    department = models.CharField(max_length=100, null=True, choices=Department)
    profile_pic = models.ImageField(upload_to=student_directory_path ,null=True, blank=True)


    def students(self):
        return [self.registration_id, self.firstname, self.lastname, self.date, self.course, self.teacher, self.year, self.faculty, self.department, self.gender]


class Attendence(models.Model):
    # teacher = models.ForeignKey(Teacher, null = True, on_delete= models.SET_NULL)
    # student = models.ForeignKey(Student, null = True, on_delete= models.SET_NULL)
    Student_ID = models.CharField(max_length=200, null=True, blank=True)
    # student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add = True, null = True)
    time = models.TimeField(auto_now_add=True, null = True)
    faculty = models.CharField(max_length=200, null = True)
    department = models.CharField(max_length=200, null = True)
    course = models.CharField(max_length=200, null = True)
    year = models.CharField(max_length=200, null = True)
    period = models.CharField(max_length=200, null = True)
    status = models.CharField(max_length=200, null = True, default='Absent')

    def attendences(self):
        return [self.Student_ID, self.date, self.time, self.faculty, self.department, self.course, self.year, self.period, self.status]