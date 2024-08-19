import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthService } from '../../_services/Auth.service'; 
import Swal from 'sweetalert2';

const Create = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleCreateAccount = async (e) => {
        e.preventDefault();
        try {
          var data = {
            username: username,
            email: email,
          };
          AuthService.createAccountService(data)
          .then(res => {
            if(res.status === 201){
              Swal.fire({ icon: 'success', title: 'Message succès', text: 'Patient ajouté avec succès.', });
              navigate('/login');
            } else {
              setError('Une erreur s\'est produite lors de la connexion.');
            }
          })
        } catch (err) {
          setError('Une erreur s\'est produite lors de la connexion. Veuillez réessayer.');
        }
    };

    return (
        <div className="container mt-5">
            <h2 className="text-center">Create Gmail Account</h2>
            <form onSubmit={handleCreateAccount}>
                <div className="form-group">
                    <label htmlFor="username">Username:</label>
                    <input
                        type="text"
                        className="form-control"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="email">Email:</label>
                    <input
                        type="email"
                        className="form-control"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" className="btn btn-primary">Create Account</button>
            </form>
            {error && <div className="alert alert-danger mt-3">{error}</div>}
            <div className="text-center mt-3">
                <p>Already have an account? <a href="/login">Login here</a>.</p>
            </div>
        </div>
    );
};

export default Create;
