import { useState, useEffect } from "react";
import { ToastContainer } from "react-bootstrap";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import LoadingSpinner from "./components/other/LoadingSpinner";
import AppRoute from "./routes/AppRoute";
import AuthRoute from "./routes/AuthRoute";
// import './App.css'

function App() {
  const [loading, setLoading] = useState(false);

  return (
    <BrowserRouter>
      {loading && <LoadingSpinner/>}
      <ToastContainer position='top-center'/>
      <Routes>    
        <Route path="/*" element={<AuthRoute/>}/>
        <Route path="/app/*" element={<AppRoute setLoading={setLoading}/>}/>
      </Routes>
    </BrowserRouter>
  )
}

export default App
