import React, { createContext, ReactNode, useContext, useState } from 'react';

interface AuthContextType {
    isAuthenticated: boolean;
    setIsAuthenticated: (value: boolean) => void;
}

// Define the default value based on the interface
const defaultValue: AuthContextType = {
    isAuthenticated: false, // Default value
    setIsAuthenticated: () => {}, // Placeholder function
};

// Create context with the default value
const AuthContext = createContext<AuthContextType>(defaultValue);

// AuthProvider component
export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    const value = { isAuthenticated, setIsAuthenticated };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Custom hook to use the auth context
export const useAuth = () => useContext(AuthContext);
