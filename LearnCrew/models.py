from django.db import models
from django.contrib.auth.models import AbstractUser

class Uloge(models.Model):
    ULOGA_KORISNIKA = (('adm', 'admin'), ('prof','profesor'), ('stud','student'))
    uloga = models.CharField(max_length=30, choices=ULOGA_KORISNIKA, blank=True)

    def __str__(self):
        return '%s' % (self.uloga, )

class Korisnici(AbstractUser):
    email = models.CharField(max_length=64)
    password = models.CharField(max_length=128)
    STATUS_STUDENTA = (('n', 'none'), ('r','redovni'), ('i','izvanredni'))
    status = models.CharField(max_length=30, choices=STATUS_STUDENTA, blank=True)
    uloga = models.ForeignKey(Uloge, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return '%s' % (self.email, )

class Predmeti(models.Model):
    name = models.CharField(max_length=255)
    kod = models.CharField(max_length=16)
    program = models.CharField(max_length=255)
    ects = models.IntegerField()
    sem_red = models.IntegerField()
    sem_izv = models.IntegerField()
    IZBORNI_PREDMET = (('Da','Da'), ('Ne','Ne'))
    izborni = models.CharField(max_length=30, choices=IZBORNI_PREDMET, blank=True)
    nositelj = models.ForeignKey(Korisnici, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.name, self.kod)

class Upisi(models.Model):
    student = models.ForeignKey(Korisnici, on_delete=models.CASCADE)
    predmet = models.ForeignKey(Predmeti, on_delete=models.CASCADE)
    status = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return '%s %s %s' % (self.student, self.predmet, self.status)