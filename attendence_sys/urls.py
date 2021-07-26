from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.register, name='register'),
    path('searchattendence/', views.searchAttendence, name='searchattendence'),
    # path('account/', views.facultyProfile, name='account'),

    path('updateStudentRedirect/', views.updateStudentRedirect, name='updateStudentRedirect'),
    path('updateStudent/', views.updateStudent, name='updateStudent'),
    path('attendence/', views.takeAttendence, name='attendence'),
    # path('check-attendance/', views.checkAttendance, name='checkattendance'),
    path('students/', views.students, name='students'),
    path('teachers/', views.teachers, name='teachers'),
    path('profile/', views.profile, name='profile'),
    path('students/studentsList', views.studentsList, name='studentList'),
    path('teachers/teacehersList', views.teachersList, name='teachersList'),
    path('addStudent/', views.addStudent, name='addStudent'),
    # path('video_feed/', views.videoFeed, name='video_feed'),
    # path('videoFeed/', views.getVideo, name='videoFeed'),
]