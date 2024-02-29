import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../users/auth'; // Adjust the path as necessary

const Logout = () => {
    const navigate = useNavigate();
    const { setIsAuthenticated } = useAuth();

    useEffect(() => {
        // Perform the logout
        sessionStorage.removeItem('token');
        setIsAuthenticated(false);
        navigate('/login');
    }, [navigate, setIsAuthenticated]);

    return null; // This component doesn't need to render anything
};

export default Logout;
