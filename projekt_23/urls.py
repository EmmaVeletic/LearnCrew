"""
URL configuration for projekt_23 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from LearnCrew import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('home/admin/', views.home_admin),
    path('home/professor/', views.home_professor),
    path('home/student/', views.home_student),
    path('list_of_subjects/', views.get_all_subjects, name='list_of_subjects'),
    path('add_subject/', views.add_subject, name='add_subject'),
    path('delete_subject/<int:subject_id>', views.delete_subject),
    path('edit_subject/<int:subject_id>', views.edit_subject),
    path('list_of_professors/', views.get_all_professors, name='list_of_professors'),
    path('add_professor/', views.add_professor, name='add_professor'),
    path('delete_professor/<int:professor_id>', views.delete_professor),
    path('edit_professor/<int:professor_id>', views.edit_professor),
    path('list_of_students/', views.get_all_students, name='list_of_students'),
    path('add_student/', views.add_student, name='add_student'),
    path('edit_student/<int:student_id>', views.edit_student, name='edit_student'),
    path('delete_student/<int:student_id>', views.delete_student, name='delete_student'),
    path('confirm_delete/<int:student_id>', views.confirmation, name='confirm_delete'),
    path('list_of_studentsSubject/<int:subject_id>', views.students_per_subject, name='list_of_studentsSubject'),
    path('list_of_subjectsProf/', views.get_all_subjects),
    path('list_of_studentsProf/<int:subject_id>', views.students_per_subject, name='list_of_studentsProf'),
    path('change_status/<int:student_id>/<int:subject_id>/', views.change_status, name='change_status'),
    path('mark_students/<int:subject_id>/<int:number>', views.mark_students),
    path('student_view/<int:student_id>/', views.enrollment_form, name='student_view'),
    path('upis/<int:student_id>/<int:subject_id>', views.upis),
    path('ispis/<int:student_id>/<int:subject_id>', views.ispis),
    path('admin_view/<int:student_id>', views.enrollment_form, name='admin_view'),
    path('change/<int:student_id>/<int:subject_id>/', views.change_to_polozen, name='change'),

]
