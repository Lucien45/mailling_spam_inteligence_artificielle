import { useEffect } from 'react';
import { Route, Routes, useLocation } from 'react-router-dom';
import Inbox from '../views/Pages/Inbox';

const AppRoute = ({setLoading}) => {
  const location = useLocation();
  useEffect(() => {
    setLoading(true);
    const handleComplete = () => {
        setLoading(false);
    };

    const timeout = setTimeout(handleComplete, 500);

    return () => {
        clearTimeout(timeout);
    };
}, [location, setLoading]);
  return (
    <Routes>
      <Route path="/inbox" element={<Inbox/>} />
    </Routes>
  )
}

export default AppRoute