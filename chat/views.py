from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
import joblib
import re
import pandas as pd
from .models import *
from .serializers import *

# Charger le modèle et le vectoriseur
MODEL_PATH = r'sample_data/logistic_regression_model.joblib'
VECTORIZER_PATH = r'sample_data/tfidf_vectorizer_regretion.joblib'
loaded_model_rf = joblib.load(MODEL_PATH)
loaded_vectorizer_rf = joblib.load(VECTORIZER_PATH)

# Fonction pour nettoyer le texte
def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', str(text))
    return text.lower()

class GmailCompteViewSet(viewsets.ModelViewSet):
    queryset = Gmail_compte.objects.all()
    serializer_class = GmailCompteSerializer

class GmailMessageViewSet(viewsets.ModelViewSet):
    queryset = Gmail_Message.objects.all()
    serializer_class = GmailMessageSerializer

class RecevoirMessageViewSet(viewsets.ModelViewSet):
    queryset = Recevoir_Message.objects.all()
    serializer_class = RecevoirMessageSerializer

class EnvoyerMessageViewSet(viewsets.ModelViewSet):
    queryset = Envoyer_Message.objects.all()
    serializer_class = EnvoyerMessageSerializer

class CreateAccount(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = GmailCompteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(date_cration=timezone.now())
            return Response({'message': 'Compte créé avec succès.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Gmail_compte.objects.get(email=email)
            request.session['user_id'] = user.id
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        except Gmail_compte.DoesNotExist:
            return Response({'error': 'Compte email n\'existe pas.'}, status=status.HTTP_404_NOT_FOUND)

class Inbox(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        user_id = request.session.get('user_id')
        if user_id is None:
            return Response({'error': 'User not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

        user = Gmail_compte.objects.get(id=user_id)
        received_messages = Recevoir_Message.objects.filter(user=user)
        serializer = RecevoirMessageSerializer(received_messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user_id = request.session.get('user_id')
        if user_id is None:
            return Response({'error': 'User not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

        selected_messages = request.data.get('selected_messages', [])
        categorie = request.data.get('categorie')
        categorie_gmail = get_object_or_404(Categorie_Gmail, Contenu=categorie)

        for message_id in selected_messages:
            message = Gmail_Message.objects.get(id=message_id)
            message.categorie = categorie_gmail
            message.save()

        return Response({'message': f'Messages marked as {categorie}.'}, status=status.HTTP_200_OK)

class SendEmail(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user_id = request.session.get('user_id')
        if user_id is None:
            return Response({'error': 'User not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

        user = Gmail_compte.objects.get(id=user_id)
        recipient_email = request.data.get('recipient')
        content = request.data.get('content')

        cleaned_content = clean_text(content)
        message_tfidf = loaded_vectorizer_rf.transform([cleaned_content])
        prediction = loaded_model_rf.predict(message_tfidf)[0]

        categorie = Categorie_Gmail.objects.get_or_create(Contenu=prediction)[0]

        try:
            recipient = Gmail_compte.objects.get(email=recipient_email)
            message = Gmail_Message.objects.create(Contenu=content, date=timezone.now(), categorie=categorie)
            Envoyer_Message.objects.create(user=user, message=message)
            Recevoir_Message.objects.create(user=recipient, message=message)
            return Response({'message': 'Email sent successfully.'}, status=status.HTTP_201_CREATED)
        except Gmail_compte.DoesNotExist:
            return Response({'error': 'Recipient not found.'}, status=status.HTTP_404_NOT_FOUND)

class Logout(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        request.session.flush()
        return Response({'message': 'Vous avez été déconnecté avec succès.'}, status=status.HTTP_200_OK)

class RetrainModel(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        original_data = pd.read_csv('sample_data/email_traduit.csv')
        original_data['Message Traduit'] = original_data['Message Traduit'].apply(clean_text)
        original_data.dropna(subset=['Category', 'Message Traduit'], inplace=True)

        df_original = original_data[['Category', 'Message Traduit']]

        messages_data = Gmail_Message.objects.all().values('Contenu', 'categorie')
        df_gmail = pd.DataFrame(list(messages_data))
        df_gmail.dropna(subset=['categorie', 'Contenu'], inplace=True)

        combined_df = pd.concat([
            df_gmail.rename(columns={'categorie': 'Category', 'Contenu': 'Message Traduit'}),
            df_original
        ], ignore_index=True)

        combined_df['Category'] = combined_df['Category'].astype(str)
        combined_df['Message Traduit'] = combined_df['Message Traduit'].astype(str)
        combined_df.dropna(subset=['Category', 'Message Traduit'], inplace=True)

        X_train, X_test, y_train, y_test = train_test_split(
            combined_df['Message Traduit'], combined_df['Category'], test_size=0.2, random_state=42
        )

        vectorizer = TfidfVectorizer()
        X_train_vec = vectorizer.fit_transform(X_train)
        X_test_vec = vectorizer.transform(X_test)

        clf_lr = LogisticRegression(random_state=42)
        clf_lr.fit(X_train_vec, y_train)

        y_pred_lr = clf_lr.predict(X_test_vec)
        accuracy = accuracy_score(y_test, y_pred_lr)
        print("Accuracy (Logistic Regression):", accuracy)
        print("Classification Report (Logistic Regression):\n", classification_report(y_test, y_pred_lr))

        joblib.dump(clf_lr, r'sample_data/logistic_regression_model.joblib')
        joblib.dump(vectorizer, r'sample_data/tfidf_vectorizer_regretion.joblib')

        return Response({'message': f'Modèle réentraîné avec succès. Précision: {accuracy:.2f}'}, status=status.HTTP_200_OK)

class UserInfo(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        user_id = request.session.get('user_id')
        if user_id is None:
            return Response({'error': 'User not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

        user = get_object_or_404(Gmail_compte, id=user_id)
        serializer = GmailCompteSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FetchCategories(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        categories = Categorie_Gmail.objects.all()
        serializer = CategorieGmailSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
