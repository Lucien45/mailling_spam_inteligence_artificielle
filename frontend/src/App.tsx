import { useState } from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import LoadingSpinner from './components/LoadingSpinner';
import AuthRoute from './routes/AuthRoute';
import AppRoute from './routes/AppRoute';
// import './App.css'

function App() {
  const [loading, setLoading] = useState<boolean>(false);

  return (
    <BrowserRouter>
      {loading && <LoadingSpinner/>}
      <ToastContainer position='top-center'/>
      <Routes>    
        <Route path="/*" element={<AuthRoute setLoading={setLoading}/>}/>
        <Route path="/app/*" element={<AppRoute setLoading={setLoading}/>}/>
      </Routes>
    </BrowserRouter>
  )
}

export default App
