from rest_framework import serializers
from .models import Gmail_compte, Gmail_Message, Recevoir_Message, Envoyer_Message, Categorie_Gmail

class GmailCompteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gmail_compte
        fields = '__all__'

class GmailMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gmail_Message
        fields = '__all__'

class RecevoirMessageSerializer(serializers.ModelSerializer):
    message = GmailMessageSerializer()

    class Meta:
        model = Recevoir_Message
        fields = '__all__'

class EnvoyerMessageSerializer(serializers.ModelSerializer):
    message = GmailMessageSerializer()

    class Meta:
        model = Envoyer_Message
        fields = '__all__'

class CategorieGmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie_Gmail
        fields = '__all__'