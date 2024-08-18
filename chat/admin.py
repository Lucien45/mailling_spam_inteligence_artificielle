from django.contrib import admin

# Register your models here.
from chat.models import *

admin.site.register(Gmail_compte)
admin.site.register(Gmail_Message)
admin.site.register(Recevoir_Message)
admin.site.register(Envoyer_Message)
admin.site.register(Categorie_Gmail)
