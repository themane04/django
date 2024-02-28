import React, {useState} from 'react';
import {BrowserRouter as Router, Routes, Route, useNavigate} from 'react-router-dom';
import Home from './home';
import Login from './users/login';
import Register from './users/register';
import Navbar from './navbar';
import axios from "axios";

const AppRouter = () => {
    const [loginError, setLoginError] = useState<string | undefined>();
    const navigate = useNavigate(); // Add this for navigation

    const handleLogin = async (email: string, password: string) => {
        try {
            const response = await axios.post('http://localhost:8000/api/login/', {
                username: email,
                password: password,
            });
            const token = response.data.token;
            console.log("Token:", token);
            localStorage.setItem('token', token); // Store the token
            // Navigate to another route or update state as needed
        } catch (error: unknown) { // Mark error as unknown type
            if (axios.isAxiosError(error)) {
                // TypeScript now knows error is an AxiosError and allows access to error.response
                console.error("Login error", error.response?.data);
                // Assuming you have a state setter function for login errors:
                setLoginError(error.response?.data.error || 'An error occurred during login.');
            } else {
                // Handle cases where the error is not an AxiosError
                console.error("An unexpected error occurred");
                setLoginError('An unexpected error occurred.');
            }
        }

    };


    return (
        <Router>
            <Navbar/>
            <div className="container mt-3">
                <Routes>
                    <Route path="/" element={<Home/>}/>
                    <Route path="/register" element={<Register/>}/>
                    <Route path="/login" element={<Login onLogin={handleLogin} errorMessage={loginError}/>}/>
                </Routes>
            </div>
        </Router>
    );
};

export default AppRouter;
