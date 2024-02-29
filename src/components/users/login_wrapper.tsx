import {useNavigate} from "react-router-dom";
import {useState} from "react";
import axios from "axios";
import Login from "./login";

export const LoginWrapper = () => {
    const navigate = useNavigate(); // Now it's safe to use useNavigate
    const [loginError, setLoginError] = useState<string | undefined>();

    const handleLogin = async (email: string, password: string) => {
        try {
            const response = await axios.post('http://localhost:8000/api/login/', {email, password});
            const token = response.data.token;
            console.log("Token:", token);
            // Store token in sessionStorage
            sessionStorage.setItem('token', token);
            // Correctly set the Authorization header using the token from sessionStorage
            axios.defaults.headers.common['Authorization'] = `Bearer ${sessionStorage.getItem('token')}`;
            // Redirect to the homepage
            navigate('/');
        } catch (error) {
            if (axios.isAxiosError(error) && error.response) {
                setLoginError(error.response?.data.error || 'An error occurred during login.');
            } else {
                setLoginError('An unexpected error occurred.');
            }
        }
    };


    return <Login onLogin={handleLogin} errorMessage={loginError}/>;
};
