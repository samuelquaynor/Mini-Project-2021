from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import Student, Attendence
from .filters import AttendenceFilter

# from django.views.decorators import gzip

from .recognizer import Recognizer
from datetime import date


@login_required(login_url='login')
def home(request):
    context = {}
    return render(request, 'attendence_sys/home.html', context)


def loginPage(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "attendence_sys/accounts/login.html", {"form": form, "msg": msg})


def register(request):

    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "attendence_sys/accounts/register.html", {"form": form, "msg": msg, "success": success})


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def updateStudentRedirect(request):
    forms = False
    context = {'forms': forms}
    if request.method == 'POST':
        try:
            reg_id = request.POST['reg_id']
            course = request.POST['course']
            student = Student.objects.get(
                registration_id=reg_id, course=course)
            updateStudentForm = CreateStudentForm(instance=student)
            context = {'form': updateStudentForm,
                       'prev_reg_id': reg_id, 'student': student}
        except:
            messages.error(request, 'Student Not Found')
            return redirect( 'attendence')
    return render(request, 'attendence_sys/student_update.html', context)


@login_required(login_url='login')
def updateStudent(request):
    forms = True
    if request.method == 'POST':
        try:
            student = Student.objects.get(
                registration_id=request.POST['prev_reg_id'])
            updateStudentForm = CreateStudentForm(
                data=request.POST, files=request.FILES, instance=student)
            if updateStudentForm.is_valid():
                updateStudentForm.save()
                messages.success(request, 'Updation Success')
                return redirect('attendence')
        except:
            messages.error(request, 'Updation Unsucessfull')
            return redirect('attendence')
    context = {'forms': forms}
    return render(request, 'attendence_sys/student_update.html', context)


@login_required(login_url='login')
def takeAttendence(request):
    if request.method == 'POST':
        details = {
            'faculty': request.POST['faculty'],
            'department': request.POST['department'],
            'course': request.POST['course'],
            'year': request.POST['year'],
            'period': request.POST['period'],
        }
        if Attendence.objects.filter(date=str(date.today()), faculty=details['faculty'], department=details['department'], course=details['course'],  year=details['year'], period=details['period']).count() != 0:
            messages.error(request, "Attendence already recorded.")
            return redirect('attendence')
        else:
            students = Student.objects.filter(
                faculty=details['faculty'], department=details['department'], course=details['course'],  year=details['year'])
            names = Recognizer(details)
            for student in students:
                if str(student.registration_id) in names:
                    attendence = Attendence(Student_ID=str(student.registration_id),
                                            period=details['period'],
                                            course=details['course'],
                                            faculty=details['faculty'],
                                            year=details['year'],
                                            department=details['department'],
                                            status='Present')
                    attendence.save()
                else:
                    attendence = Attendence(Student_ID=str(student.registration_id),
                                            period=details['period'],
                                            course=details['course'],
                                            faculty=details['faculty'],
                                            year=details['year'],
                                            department=details['department'])
                    attendence.save()
            attendences = Attendence.objects.filter(date=str(date.today(
            )), faculty=details['faculty'], department=details['department'], course=details['course'],  year=details['year'])
            context = {"attendences": attendences, "ta": True}
            messages.success(request, "Attendence taking Success")
            return render(request, 'attendence_sys/attendence.html', context)
    context = {}
    return render(request, 'attendence_sys/check-attendance.html', context)


def searchAttendence(request):
    attendences = Attendence.objects.all()
    myFilter = AttendenceFilter(request.GET, queryset=attendences)
    attendences = myFilter.qs
    context = {'myFilter': myFilter, 'attendences': attendences, 'ta': False}
    return render(request, 'attendence_sys/attendence.html', context)


# def facultyProfile(request):
#     faculty = request.user.faculty
#     form = FacultyForm(instance = faculty)
#     context = {'form':form}
#     return render(request, 'attendence_sys/facultyForm.html', context)


# @login_required(login_url='login')
# def checkAttendance(request):

#     context = {}
#     return render(request, 'attendence_sys/check-attendance.html', context)


@login_required(login_url='login')
def students(request):
    attendences = Attendence.objects.all()
    present = 0
    absent = 0
    for attendence in attendences:
        if attendence.status == 'Present':
            present += 1
        elif attendence.status == 'Absent':
            absent += 1
    students = Teacher.objects.get(
        username=request.user.username).students.all()
    context = {'students': students.values, 'attendences': attendences, 'present': present, 'absent': absent}
    return render(request, 'attendence_sys/students/students.html', context)


@login_required(login_url='login')
def teachers(request):
    context = {}
    return render(request, 'attendence_sys/teachers/teachers.html', context)


@login_required(login_url='login')
def profile(request):
    context = {}
    return render(request, 'attendence_sys/profile.html', context)


# @login_required(login_url='login')
# def studentsList(request):
#     students = Teacher.objects.get(
#         username=request.user.username).students.all()
#     context = {'students': students.values}
#     return render(request, 'attendence_sys/students/student_list.html', context)


@login_required(login_url='login')
def teachersList(request):
    context = {}
    return render(request, 'attendence_sys/teachers/teachers_list.html', context)


@login_required(login_url='login')
def addStudent(request):
    studentForm = CreateStudentForm()

    if request.method == 'POST':
        studentForm = CreateStudentForm(data=request.POST, files=request.FILES)
        # print(request.POST)
        stat = False
        try:
            student = Student.objects.get(
                registration_id=request.POST['registration_id'])
            stat = True
        except:
            stat = False
        if studentForm.is_valid() and (stat == False):
            studentForm.save()
            name = studentForm.cleaned_data.get(
                'firstname') + " " + studentForm.cleaned_data.get('lastname')
            messages.success(request, 'Student ' + name +
                             ' was successfully added.')
            return redirect('attendence')
        else:
            messages.error(request, 'Student with Registration Id ' +
                           request.POST['registration_id']+' already exists.')
            return redirect('studentList')
    context = {'studentForm': studentForm}
    return render(request, 'attendence_sys/students/add_student.html', context)

# @login_required(login_url = 'login')
# def updateStudent(request):
#     context = {}
#     return render(request, 'attendence_sys/students/add_student.html', context)


# class VideoCamera(object):z
#     def __init__(self):
#         self.video = cv2.VideoCapture(0)
#     def __del__(self):
#         self.video.release()

#     def get_frame(self):
#         ret,image = self.video.read()
#         ret,jpeg = cv2.imencode('.jpg',image)
#         return jpeg.tobytes()


# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         yield(b'--frame\r\n'
#         b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# @gzip.gzip_page
# def videoFeed(request):
#     try:
#         return StreamingHttpResponse(gen(VideoCamera()),content_type="multipart/x-mixed-replace;boundary=frame")
#     except:
#         print("aborted")

# def getVideo(request):
#     return render(request, 'attendence_sys/videoFeed.html')
