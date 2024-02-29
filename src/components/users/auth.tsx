// Import React dependencies
import React, {createContext, ReactNode, useContext, useState, useEffect} from 'react';
import axios from "axios";

interface AuthContextType {
    isAuthenticated: boolean;
    setIsAuthenticated: (value: boolean) => void;
}

const defaultValue: AuthContextType = {
    isAuthenticated: false,
    setIsAuthenticated: () => {
    },
};


const AuthContext = createContext<AuthContextType>(defaultValue);

export const AuthProvider = ({children}: { children: ReactNode }) => {
    // Initialize isAuthenticated based on the presence of a token in sessionStorage
    const [isAuthenticated, setIsAuthenticated] = useState<boolean>(!!sessionStorage.getItem('token'));

    // Optionally, sync isAuthenticated state with sessionStorage on app load
    useEffect(() => {
        const token = sessionStorage.getItem('token');
        setIsAuthenticated(!!token);
    }, []);

    const value = {isAuthenticated, setIsAuthenticated};

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => useContext(AuthContext);
