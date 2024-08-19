import Axios from "./Axios";

// Service pour récupérer les messages de la boîte de réception
let fetchMessages = () => {
    return Axios.get('/api/inbox/');
};

// Service pour mettre à jour la catégorie des messages sélectionnés
let updateCategory = (data) => {
    return Axios.post('/api/inbox/', data);
};

// Service pour envoyer un e-mail
let sendEmailService = (data) => {
    return Axios.post('/api/send-email/', data);
};

// Service pour réentraîner le modèle
let retrainModelService = () => {
    return Axios.post('/api/retrain-model/');
};

// Service pour récupérer les infos utilisateur
let fetchUserInfo = () => {
    return Axios.get('/api/user-info/');
};

// Service pour récupérer les catégories
let fetchCategories = () => {
    return Axios.get('/api/categories/');
};

export const InboxService = {
    fetchMessages, 
    updateCategory, 
    sendEmailService, 
    retrainModelService, 
    fetchUserInfo, 
    fetchCategories
};
