import React from 'react';
import AppRouter from './components/router'
import 'bootstrap/dist/css/bootstrap.min.css';
import {AuthProvider} from "./components/users/auth";


const App: React.FC = () => {
    return (
        <AuthProvider>
            <AppRouter/>
        </AuthProvider>
    );
};

export default App;
