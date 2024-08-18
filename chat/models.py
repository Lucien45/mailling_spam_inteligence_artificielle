from django.db import models
from django.utils import timezone

# Create your models here.
class Gmail_compte(models.Model):
    """
    Description: Model Gmail_compte
    """
    username = models.CharField(max_length=50, blank=False, verbose_name="username")
    email = models.EmailField(unique=True, max_length=255, blank=False)
    date_cration = models.DateTimeField(blank=True, null=True)

    class Meta:
        pass
    
class Categorie_Gmail(models.Model):
    """
    Description: Model Envoyer_Message
    """
    Contenu = models.TextField(max_length=50, unique=True, blank=True, null=True)
    
class Gmail_Message(models.Model):
    """
    Description: Model Gmail_Message
    """
    Contenu = models.TextField(blank=True)
    date = models.DateTimeField(blank=True, null=True)
    categorie = models.ForeignKey(Categorie_Gmail, on_delete=models.CASCADE, blank=True, null=True)


    class Meta:
        pass

class Recevoir_Message(models.Model):
    """
    Description: Model Recevoir_Message
    """
    user = models.ForeignKey(Gmail_compte, on_delete=models.CASCADE)
    message = models.ForeignKey(Gmail_Message, on_delete=models.CASCADE)

    class Meta:
        pass

class Envoyer_Message(models.Model):
    """
    Description: Model Envoyer_Message
    """
    user = models.ForeignKey(Gmail_compte, on_delete=models.CASCADE)
    message = models.ForeignKey(Gmail_Message, on_delete=models.CASCADE, related_name='envoyer_message_set')
