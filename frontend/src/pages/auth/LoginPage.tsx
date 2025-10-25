/* eslint-disable @typescript-eslint/no-unused-vars */
import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import Swal from "sweetalert2";

const LoginPage = () => {
    const [email, setEmail] = useState('');
    const [error, setError] = useState<string | null>(null);
    const navigate = useNavigate();

    const handleLogin = async (e: FormEvent) => {
        e.preventDefault();
        try {
            const data = {
                email: email,
            };
            // AuthService.loginService(data)
            // .then(res => {
            //     console.log(res);
            //     if(res.status === 200){
                Swal.fire({ icon: 'success', title: 'Message succès', text: 'connexion reussi avec succès.', });
                navigate('/app/inbox');
            //     } else {
            //     setError('Une erreur s\'est produite.');
            //     }
            // })
        } catch (err) {
            console.log(err);
            setError('Une erreur s\'est produite lors de la connexion. Veuillez réessayer.');
        }
    };

    return (
        <div className="container mt-5">
            <h2 className="text-center">Login</h2>
            <form onSubmit={handleLogin}>
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
                <button type="submit" className="btn btn-primary">Login</button>
            </form>
            {error && <div className="alert alert-danger mt-3">{error}</div>}
            <div className="text-center mt-3">
                <p>Don't have an account? <a href="/create-account">Create one here</a>.</p>
            </div>
        </div>
    )
}

export default LoginPage