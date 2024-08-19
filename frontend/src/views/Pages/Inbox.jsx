import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { InboxService } from '../../_services/Inbox.service'; 
import { AuthService } from '../../_services/Auth.service'; 
import Swal from 'sweetalert2';

const Inbox = () => {
    const [user, setUser] = useState({ username: '', email: '' });
    const [categories, setCategories] = useState([]);
    const [messages, setMessages] = useState([]);
    const [selectedMessages, setSelectedMessages] = useState([]);
    const [category, setCategory] = useState('');
    const [recipient, setRecipient] = useState('');
    const [content, setContent] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        getInfoUser();
        getCategories();
        getMessages();
    }, []);

    const getInfoUser = async () => {
        try {
            const res = await InboxService.fetchUserInfo();
            console.log('user: ', res);
            setUser(res.data);
        } catch (error) {
            Swal.fire({ icon: 'error', title: 'Erreur!', text: `Échec de récupération: ${error}` });
            console.error(error);
        }
    };

    const getCategories = async () => {
        try {
            const res = await InboxService.fetchCategories();
            console.log('catégorie: ', res.data);
            setCategories(res.data);
        } catch (error) {
            Swal.fire({ icon: 'error', title: 'Erreur!', text: `Échec de récupération: ${error}` });
            console.error(error);
        }
    };

    const getMessages = async () => {
        try {
            const res = await InboxService.fetchMessages();
            console.log('message: ', res);
            setMessages(res.data);
        } catch (error) {
            Swal.fire({ icon: 'error', title: 'Erreur!', text: `Échec de récupération: ${error}` });
            console.error(error);
        }
    };

    const handleLogout = async () => {
        try {
            const res = await AuthService.logoutService();
            if(res.status === 200){
                Swal.fire({ icon: 'success', title: 'Message succès', text: 'Déconnexion réussie.' });
                navigate('/login');
            } else {
                Swal.fire({ icon: 'error', title: 'Erreur!', text: 'Une erreur s\'est produite lors de la déconnexion.' });
            }
        } catch (error) {
            Swal.fire({ icon: 'error', title: 'Erreur de connexion', text: 'Une erreur s\'est produite lors de la connexion. Veuillez réessayer.' });
        }
    };

    const handleCategoryUpdate = async (e) => {
        e.preventDefault();
        try {
            const data = {
                message: selectedMessages,
                categorie: category,
            };
            const res = await InboxService.updateCategory(data);
            console.log(res);
            if(res.status === 200){
                Swal.fire({ icon: 'success', title: 'Message succès', text: 'Mise à jour effectuée avec succès.' });
            } else {
                Swal.fire({ icon: 'error', title: 'Erreur!', text: 'Une erreur s\'est produite lors de la mise à jour.' });
            }
        } catch (error) {
            Swal.fire({ icon: 'error', title: 'Erreur de connexion', text: 'Une erreur s\'est produite lors de la connexion. Veuillez réessayer.' });
        }
    };

    const handleSendEmail = async (e) => {
        e.preventDefault();
        try {
            const data = {
                recipient: recipient,
                content: content,
            };
            const res = await InboxService.sendEmailService(data);
            console.log(res);
            if(res.status === 201){
                Swal.fire({ icon: 'success', title: 'Message succès', text: 'L\'e-mail a été envoyé avec succès.' });
            } else {
                Swal.fire({ icon: 'error', title: 'Erreur!', text: 'Une erreur s\'est produite lors de l\'envoi de l\'e-mail.' });
            }
        } catch (error) {
            Swal.fire({ icon: 'error', title: 'Erreur de connexion', text: 'Une erreur s\'est produite lors de la connexion. Veuillez réessayer.' });
        }
    };

    const handleRetrainModel = async () => {
        try {
            const res = await InboxService.retrainModelService();
            if(res.status === 200){
                Swal.fire({ icon: 'success', title: 'Message succès', text: 'Réentraînement effectué.' });
            } else {
                Swal.fire({ icon: 'error', title: 'Erreur!', text: 'Une erreur s\'est produite lors du réentraînement.' });
            }
        } catch (error) {
            Swal.fire({ icon: 'error', title: 'Erreur de connexion', text: 'Une erreur s\'est produite lors de la connexion. Veuillez réessayer.' });
        }
    };

    return (
        <div className="container mt-5">
            <div className="d-flex justify-content-between">
                <h2 className="text-center">Boîte de Réception</h2>
                <button onClick={handleLogout} className="btn btn-danger">Déconnexion</button>
            </div>
            <p>{user.username} | {user.email}</p>
            <button onClick={handleRetrainModel} className="btn btn-success mb-3">Réentraîner Modèle</button>
            <form onSubmit={handleCategoryUpdate}>
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>Select</th>
                            <th>Expéditeur</th>
                            <th>Message</th>
                            <th>Date</th>
                            <th>Catégorie</th>
                        </tr>
                    </thead>
                    <tbody>
                        {messages.map((msg, index) => (
                            <tr key={index}>
                                <td>
                                    <input 
                                        type="checkbox" 
                                        value={msg.id}
                                        onChange={(e) => {
                                            if(e.target.checked) {
                                                setSelectedMessages([...selectedMessages, msg.id]);
                                            } else {
                                                setSelectedMessages(selectedMessages.filter(id => id !== msg.id));
                                            }
                                        }}
                                    />
                                </td>
                                <td>{msg.sender}</td>
                                <td>{msg.content}</td>
                                <td>{msg.date}</td>
                                <td>{msg.categorie || 'Non classé'}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                <div className="form-group">
                    <label>Catégorie:</label>
                    <select className="form-control" value={category} onChange={(e) => setCategory(e.target.value)}>
                        <option value="">Sélectionnez une catégorie</option>
                        {categories.map((cat, index) => (
                            <option key={index} value={cat.id}>{cat.Contenu}</option>
                        ))}
                    </select>
                </div>
                <button type="submit" className="btn btn-primary mt-3">Mettre à jour</button>
            </form>
            <form onSubmit={handleSendEmail}>
                <h4>Envoyer un Email</h4>
                <div className="form-group">
                    <label>Destinataire:</label>
                    <input 
                        type="text" 
                        className="form-control" 
                        value={recipient}
                        onChange={(e) => setRecipient(e.target.value)}
                    />
                </div>
                <div className="form-group">
                    <label>Contenu:</label>
                    <textarea 
                        className="form-control" 
                        rows="4"
                        value={content}
                        onChange={(e) => setContent(e.target.value)}
                    ></textarea>
                </div>
                <button type="submit" className="btn btn-primary mt-3">Envoyer</button>
            </form>
        </div>
    );
};

export default Inbox;
