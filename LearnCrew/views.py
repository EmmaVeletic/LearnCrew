from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import UserForm, SubjectForm
from django.contrib.auth.decorators import login_required
from django.http import *
from .models import Predmeti, Korisnici, Upisi
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def register(request):
    if request.method == 'GET':
        form = UserForm()
        return render(request, 'register.html', {"form": form})
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data.get('password'))
            form.save()
            return redirect('login')
        else:
            return redirect('register')
    else:
        return HttpResponseNotAllowed('Something is wrong')

def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Hi {username}, welcome back!")
                return redirect('home')

        messages.error(request, "Invalid username or password!")
        return render(request, 'login.html', {'form': form})

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

def home(request):
    if str(request.user.uloga) == 'adm':
        url = 'admin/'
    elif str(request.user.uloga) == 'prof':
        url = 'professor/'
    elif str(request.user.uloga) == 'stud':
        url = 'student/'
    else:
        return HttpResponseNotAllowed("You are not allowed")
    return redirect(url)


def home_admin(request):
    return render(request, 'admin.html')

def home_professor(request):
    return render(request, 'professor.html')

def home_student(request):
    student_id = request.user.id
    return render(request, 'student.html', {"student_id": student_id})

def get_all_subjects(request):
    if str(request.user.uloga) == 'adm':
        subjects = Predmeti.objects.all()
        return render(request, 'list_of_subjects.html', {"data": subjects})
    elif str(request.user.uloga) == 'prof':
        professor_id = request.user.id
        professor = Korisnici.objects.get(id=professor_id)
        print(professor)
        subjects = Predmeti.objects.filter(nositelj=professor)
        print(subjects)
        return render(request, 'list_of_subjectsProf.html', {"data": subjects})


def add_subject(request):
    if request.method == 'GET':
        form = SubjectForm()
        return render(request, 'add_subject.html', {"form": form})
    elif request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_of_subjects')
        else:
            messages.error(request, "Invalid data for subject!")
            return render(request, 'add_subject.html', {'form': form})
    else:
        return HttpResponseNotAllowed()

def edit_subject(request, subject_id):
    subject = Predmeti.objects.get(pk=subject_id)
    if request.method == 'GET':
        form = SubjectForm(instance=subject)
        return render(request, 'add_subject.html', {"form": form})
    elif request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
        return redirect('list_of_subjects')
    else:
        return HttpResponseNotAllowed()


def delete_subject(request, subject_id):
    Predmeti.objects.filter(id=subject_id).delete()
    return redirect('list_of_subjects')

def get_all_professors(request):
    professors = Korisnici.objects.filter(uloga=2)
    return render(request, 'list_of_professors.html', {"data": professors})

def add_professor(request):
    initial_dict = {
        "uloga": 2,
        "status": "n"
    }

    if request.method == 'GET':
        form = UserForm(initial=initial_dict)
        return render(request, 'add_professor.html', {"form": form})
    elif request.method == 'POST':
        form = UserForm(request.POST, initial=initial_dict)
        if form.is_valid():
            #form.cleaned_data['uloga'] = 'prof'
            form.save()
            return redirect('list_of_professors')
        else:
            messages.error(request, "Invalid data!")
            return render(request, 'add_professor.html', {'form': form})
    else:
        return HttpResponse("Something is wrong, please contact our service")


def edit_professor(request, professor_id):
    professor = Korisnici.objects.get(pk=professor_id)
    if request.method == 'GET':
        form = UserForm(instance=professor)
        return render(request, 'add_professor.html', {"form": form})
    elif request.method == 'POST':
        form = UserForm(request.POST, instance=professor)
        if form.is_valid():
            form.save()
        return redirect('list_of_professors')
    else:
        return HttpResponse("Something is wrong, please contact our service")

def delete_professor(request, professor_id):
    Korisnici.objects.filter(id=professor_id).delete()
    return redirect('list_of_professors')

def get_all_students(request):
    students = Korisnici.objects.filter(uloga=3)
    return render(request, 'list_of_students.html', {"data": students})

def add_student(request):
    initial_dict = {
        "uloga": 3,
    }

    if request.method == 'GET':
        form = UserForm(initial=initial_dict)
        return render(request, 'add_student.html', {"form": form})
    elif request.method == 'POST':
        form = UserForm(request.POST, initial=initial_dict)
        if form.is_valid():
            form.save()
            return redirect('list_of_students')
        else:
            messages.error(request, "Invalid data!")
            return render(request, 'add_student.html', {'form': form})
    else:
        return HttpResponse("Something is wrong, please contact our service")

def edit_student(request, student_id):
    student = Korisnici.objects.get(pk=student_id)
    if request.method == 'GET':
        form = UserForm(instance=student)
        return render(request, 'add_student.html', {"form": form})
    elif request.method == 'POST':
        form = UserForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
        return redirect('list_of_students')
    else:
        return HttpResponse("Something is wrong, please contact our service")

def delete_student(request, student_id):
    if 'Yes' in request.POST:
        Korisnici.objects.filter(id=student_id).delete()
        messages.success(request, 'Successfully deleted!')
    return redirect('list_of_students')

#samo za studenta
def confirmation(request, student_id):
    if request.method == 'GET':
        return render(request, 'confirm_delete.html', {"data": student_id})
    return HttpResponseNotAllowed()

def students_per_subject(request, subject_id):
    if str(request.user.uloga) == 'adm':
        upisi = Upisi.objects.filter(predmet=subject_id)
        return render(request, 'list_of_students_per_subject.html', {"data": upisi})
    elif str(request.user.uloga) == 'prof':
        upisi = Upisi.objects.filter(predmet=subject_id).filter(status="upisan")
        return render(request, 'list_of_studentsProf.html', {"data": upisi, "subject_id": subject_id})

def change_status(request, student_id, subject_id):
    status = request.POST.get('status')
    print(status)
    upisi = Upisi.objects.filter(student=student_id).filter(predmet=subject_id)
    print(upisi)

    if status == "izgubio potpis":
        new_status = "izgubio potpis"
        Upisi.objects.filter(student=student_id).filter(predmet=subject_id).update(status=new_status)
    elif status == "polozen":
        new_status = "polozen"
        Upisi.objects.filter(student=student_id).filter(predmet=subject_id).update(status=new_status)
    elif status == "upisan":
        new_status = "upisan"
        Upisi.objects.filter(student=student_id).filter(predmet=subject_id).update(status=new_status)

    if str(request.user.uloga) == "prof":
        messages.success(request, 'Default menu')
        return redirect('/list_of_studentsProf/' + str(subject_id))


def change_to_polozen(request, student_id, subject_id):
    Upisi.objects.filter(student=student_id).filter(predmet=subject_id).update(status="polozen")
    return redirect('/admin_view/' + str(student_id))


def mark_students(request, subject_id, number):
    if number == 1:
        upisi = Upisi.objects.filter(predmet=subject_id).filter(status="izgubio potpis")
    elif number == 2:
        upisi = Upisi.objects.filter(predmet=subject_id).filter(status="upisan")
        messages.success(request, 'Default menu')
    else:
        upisi = Upisi.objects.filter(predmet=subject_id).filter(status="polozen")

    return render(request, 'list_of_studentsProf.html', {"data": upisi, "subject_id": subject_id})

def enrollment_form(request, student_id):
    if str(request.user.uloga) == "stud":
        user_id = request.user.id
        template = 'student_view.html'

    if str(request.user.uloga) == "adm":
        user_id = student_id
        template = 'admin_view.html'

    user = Korisnici.objects.get(id=user_id)
    status = user.status
    upisani_predmeti = Upisi.objects.filter(student=user_id).filter(status="upisan") | Upisi.objects.filter(student=user_id).filter(status="polozen")
    first, second, third, forth, fifth, sixth, seventh, eighth = ([] for i in range(8))
    if status == "r":
        for upis in upisani_predmeti:
            if upis.predmet.sem_red == 1:
                first.append(upis)
            elif upis.predmet.sem_red == 2:
                second.append(upis)
            elif upis.predmet.sem_red == 3:
                third.append(upis)
            elif upis.predmet.sem_red == 4:
                forth.append(upis)
            elif upis.predmet.sem_red == 5:
                fifth.append(upis)
            else:
                sixth.append(upis)
    elif status == "i":
        for upis in upisani_predmeti:
            if upis.predmet.sem_izv == 1 and upis not in first:
                first.append(upis)
            elif upis.predmet.sem_izv == 2:
                second.append(upis)
            elif upis.predmet.sem_izv == 3:
                third.append(upis)
            elif upis.predmet.sem_izv == 4:
                forth.append(upis)
            elif upis.predmet.sem_izv == 5:
                fifth.append(upis)
            elif upis.predmet.sem_izv == 6:
                sixth.append(upis)
            elif upis.predmet.sem_izv == 7:
                seventh.append(upis)
            else:
                eighth.append(upis)

    neupisani_predmeti= []
    predmeti = Predmeti.objects.all()
    #print(predmeti)
    for predmet in predmeti:
        if upisani_predmeti:
            for upis in upisani_predmeti:
                if predmet != upis.predmet and predmet not in neupisani_predmeti:
                    neupisani_predmeti.append(predmet)
        else:
            neupisani_predmeti.append(predmet)
    #print(neupisani_predmeti)
    return render(request, template, {"neupisani": neupisani_predmeti, "student_id": user_id, "student": user, "first": first,
                                          "second": second, "third": third, "forth": forth, "fifth": fifth,
                                          "sixth": sixth, "seventh": seventh, "eighth": eighth})

def upis(request, student_id, subject_id):
    user_id = request.user.id
    user = Korisnici.objects.get(id=student_id)
    subject = Predmeti.objects.get(id=subject_id)
    if not Upisi.objects.filter(predmet=subject).filter(student=user):
        upis = Upisi(student=user, predmet=subject, status="upisan")
        upis.save()
        print("Save")
    if str(request.user.uloga) == "stud":
        return redirect('/student_view/' + str(user_id))
    elif str(request.user.uloga) == "adm":
        return redirect('/admin_view/' + str(student_id))

def ispis(request, student_id, subject_id):
    user_id = request.user.id
    user = Korisnici.objects.get(id=student_id)
    subject = Predmeti.objects.get(id=subject_id)
    Upisi.objects.filter(student=user).filter(predmet=subject).delete()
    print("Delete")
    if str(request.user.uloga) == "stud":
        return redirect('/student_view/' + str(user_id))
    elif str(request.user.uloga) == "adm":
        return redirect('/admin_view/' + str(student_id))

















