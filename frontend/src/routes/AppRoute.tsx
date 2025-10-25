import { useEffect } from "react";
import { Route, Routes, useLocation } from "react-router-dom";
import Inbox from "../pages/home";

interface AppRouteProps {
    setLoading: (value: boolean) => void;
}

const AppRoute = ({setLoading}: AppRouteProps) => {

    const location = useLocation();

    useEffect(() => {
        setLoading(true);
        const handleComplete = () => setLoading(false);
        const timeout = setTimeout(handleComplete, 500);

        return () => clearTimeout(timeout);
    }, [location, setLoading]);

    return (
        <Routes>
            <Route path="/inbox" element={<Inbox/>} />
        </Routes>
    )
}

export default AppRoute