import Axios from "./Axios";

// Service for creating a new account
let createAccountService = (data) => {
    return Axios.post('/api/create-account/', data)
}

// Service for logging in
let loginService = (data) => {
    return Axios.post('/api/login/', data)
}

// Service for logging out
let logoutService = () => {
    return Axios.post('/api/logout/')
}

export const AuthService = {
    createAccountService, loginService, logoutService
}
