import React from 'react';
import {BrowserRouter as Router, Routes, Route, useNavigate} from 'react-router-dom';
import Home from './home/home';
import Register from './users/register';
import Navbar from './navbar';
import {LoginWrapper} from "./wrappers/login_wrapper";


const AppRouter = () => {
    return (
        <Router>
            <Navbar/>
            <div className="container mt-3">
                <Routes>
                    <Route path="/" element={<Home/>}/>
                    <Route path="/register" element={<Register/>}/>
                    <Route path="/login" element={<LoginWrapper/>}/>
                </Routes>
            </div>
        </Router>
    );
};

export default AppRouter;
