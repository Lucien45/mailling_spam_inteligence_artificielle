import joblib
import re
import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split

from chat.models import *

# Charger le modèle et le vectoriseur
MODEL_PATH = r'sample_data/logistic_regression_model.joblib'
VECTORIZER_PATH = r'sample_data/tfidf_vectorizer_regretion.joblib'
loaded_model_rf = joblib.load(MODEL_PATH)
loaded_vectorizer_rf = joblib.load(VECTORIZER_PATH)

# Fonction pour nettoyer le texte
def clean_text(text):
    # Supprimer les caractères spéciaux, les chiffres, et convertir en minuscules
    text = re.sub(r'[^a-zA-Z\s]', '', str(text))
    return text.lower()

def create_account(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        if not Gmail_compte.objects.filter(email=email).exists():
            Gmail_compte.objects.create(username=username, email=email, date_cration=timezone.now())
            messages.success(request, 'Compte créé avec succès.')
            return redirect('login')
        else:
            messages.error(request, 'compte Email existe déjà.')
    return render(request, 'create_accounts.html')


def login(request):
    error = None
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = Gmail_compte.objects.get(email=email)
            request.session['user_id'] = user.id
            return redirect('inbox')
        except Gmail_compte.DoesNotExist:
            error = 'compte email n\'existe pas.'
    return render(request, 'login.html', {'error': error})

def inbox(request):
    # Récupérer l'identifiant utilisateur de la session
    user_id = request.session.get('user_id')
    
    if user_id is None:
        return redirect('login')

    # Récupérer l'utilisateur de la base de données à l'aide de l'user_id
    user = Gmail_compte.objects.get(id=user_id)
    received_messages = Recevoir_Message.objects.filter(user=user)
    
    if request.method == 'POST':
        selected_messages = request.POST.getlist('selected_messages')
        categorie = request.POST.get('categorie')
        categorie_gmail = get_object_or_404(Categorie_Gmail, Contenu=categorie)

        for message_id in selected_messages:
            message = Gmail_Message.objects.get(id=message_id)
            message.categorie = categorie_gmail
            message.save()

        messages.success(request, f'Messages marqués comme {categorie}.')
        return redirect('inbox')

    context = {
        'user': user,
        'received_messages': received_messages,
        'categories': Categorie_Gmail.objects.all(),
    }
    
    return render(request, 'inbox.html', context)

def send_email(request):
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect('login')

    user = Gmail_compte.objects.get(id=user_id)

    if request.method == 'POST':
        recipient_email = request.POST['recipient']
        content = request.POST['content']

        # Nettoyer le contenu et prédire la catégorie
        cleaned_content = clean_text(content)
        message_tfidf = loaded_vectorizer_rf.transform([cleaned_content])
        prediction = loaded_model_rf.predict(message_tfidf)[0]

        # Déterminer la catégorie (en supposant que « ham » et « spam » sont les deux catégories)
        categorie = Categorie_Gmail.objects.get_or_create(Contenu=prediction)[0]

        try:
            recipient = Gmail_compte.objects.get(email=recipient_email)
            message = Gmail_Message.objects.create(Contenu=content, date=timezone.now(), categorie=categorie)
            Envoyer_Message.objects.create(user=user, message=message)
            Recevoir_Message.objects.create(user=recipient, message=message)
            messages.success(request, 'Email sent successfully.')
        except Gmail_compte.DoesNotExist:
            messages.error(request, 'Recipient not found.')

    return redirect('inbox')

def logout_view(request):
    # Effacer les données de session
    request.session.flush()
    # Redirection vers la page de connexion
    messages.info(request, 'Vous avez été déconnecté avec succès.')
    return redirect('login')

# Rentrainement du modele avec la nouvelle donnees du Gmail_Message
def retrain_modele(request):
    # Charger les données du modèle Gmail_Message
    messages_data = Gmail_Message.objects.all().values('Contenu', 'categorie')

    # Convertir en DataFrame
    df = pd.DataFrame(list(messages_data))

    # Diviser les données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(
        df['Contenu'], df['categorie'], test_size=0.2, random_state=42
    )

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Entraînement du modèle RandomForestClassifier
    clf_rf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf_rf.fit(X_train_vec, y_train)

    # Test du modèle
    y_pred_rf = clf_rf.predict(X_test_vec)

    # Évaluation des performances du modèle
    accuracy = accuracy_score(y_test, y_pred_rf)
    print("Accuracy (RandomForest):", accuracy)
    print("Classification Report (RandomForest):\n", classification_report(y_test, y_pred_rf))

    # Sauvegarde du modèle entraîné avec joblib
    joblib.dump(clf_rf, r'sample_data/logistic_regression_model.joblib')
    joblib.dump(vectorizer, r'sample_data/tfidf_vectorizer_regretion.joblib')

    print("Modèle RandomForest et vectorizer sauvegardés.")

    # Display success message
    messages.success(request, f'Modèle réentraîné avec succès. Précision: {accuracy:.2f}')

    # Redirect back to inbox or desired page
    return redirect('inbox')

# Rentrainement du modele avec la nouvelle donnees du Gmail_Message et l'encien email_traduit.csv
def retrain_model(request):
    # Étape 1: Charger les données originales depuis email_traduit.csv
    original_data = pd.read_csv('sample_data/email_traduit.csv')
    
    # Nettoyage du texte
    original_data['Message Traduit'] = original_data['Message Traduit'].apply(clean_text)
    
    # Vérification des valeurs manquantes
    original_data.dropna(subset=['Category', 'Message Traduit'], inplace=True)

    # Sélectionner les colonnes d'intérêt
    df_original = original_data[['Category', 'Message Traduit']]

    # Étape 2: Charger les données du modèle Gmail_Message
    messages_data = Gmail_Message.objects.all().values('Contenu', 'categorie')
    df_gmail = pd.DataFrame(list(messages_data))
    
    # Vérification des valeurs manquantes
    df_gmail.dropna(subset=['categorie', 'Contenu'], inplace=True)

    # Combine the data
    combined_df = pd.concat([
        df_gmail.rename(columns={'categorie': 'Category', 'Contenu': 'Message Traduit'}),
        df_original
    ], ignore_index=True)

    # Convert 'Category' and 'Message Traduit' to strings to ensure consistency
    combined_df['Category'] = combined_df['Category'].astype(str)
    combined_df['Message Traduit'] = combined_df['Message Traduit'].astype(str)

    # Vérification des valeurs manquantes dans le dataframe combiné
    combined_df.dropna(subset=['Category', 'Message Traduit'], inplace=True)

    # Étape 3: Diviser les données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(
        combined_df['Message Traduit'], combined_df['Category'], test_size=0.2, random_state=42
    )

    # Étape 4: TF-IDF Vectorization
    vectorizer = TfidfVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Étape 5: Entraînement du modèle LogisticRegression
    clf_lr = LogisticRegression(random_state=42)
    clf_lr.fit(X_train_vec, y_train)

    # Étape 6: Test du modèle et Évaluation de sa performance
    y_pred_lr = clf_lr.predict(X_test_vec)
    accuracy = accuracy_score(y_test, y_pred_lr)
    print("Accuracy (Logistic Regression):", accuracy)
    print("Classification Report (Logistic Regression):\n", classification_report(y_test, y_pred_lr))

    # Étape 7: Sauvegarde du modèle entraîné avec joblib
    joblib.dump(clf_lr, r'sample_data/logistic_regression_model.joblib')
    joblib.dump(vectorizer, r'sample_data/tfidf_vectorizer_regretion.joblib')

    print("Logistic Regression model and vectorizer saved.")

    # Display success message
    messages.success(request, f'Modèle réentraîné avec succès. Précision: {accuracy:.2f}')

    # Redirect back to inbox or desired page
    return redirect('inbox')
