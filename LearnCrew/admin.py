from django.contrib import admin
from .models import Korisnici, Upisi, Uloge, Predmeti

admin.site.register(Korisnici)
admin.site.register(Upisi)
admin.site.register(Uloge)
admin.site.register(Predmeti)
