import { useEffect } from 'react'
import { Route, Routes, useLocation } from 'react-router-dom';
import LoginPage from '../pages/auth/LoginPage';
import Page404 from '../pages/other/Page404';
import RegisterPage from '../pages/auth/RegisterPage';

interface AutRouteProps {
    setLoading: (value: boolean) => void;
}

const AuthRoute = ({setLoading}: AutRouteProps) => {
    const location = useLocation();

    useEffect(() => {
        setLoading(true);
        const handleComplete = () => setLoading(false);
        const timeout = setTimeout(handleComplete, 500);

        return () => clearTimeout(timeout);
    }, [location, setLoading]);
    return (
        <Routes>
            <Route path='/' element={<LoginPage/>}/>
            <Route path="/login" element={<LoginPage />} />
            <Route path='/create-account' element={<RegisterPage/>}/>
            <Route path='*' element={<Page404/>}/>
        </Routes>
    )
}

export default AuthRoute