import React from 'react';
import {Link, useNavigate} from 'react-router-dom';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faBell} from '@fortawesome/free-solid-svg-icons';
import {useAuth} from "./users/auth";
import Dropdown from "react-bootstrap/Dropdown";


interface NavbarProps {
    isAuthenticated?: boolean;
    username?: string;
    profilePic?: string;
}

const Navbar: React.FC<NavbarProps> = ({username, profilePic}) => {
    const defaultProfilePic = 'default_profile_picture.jpg';
    const {isAuthenticated, setIsAuthenticated} = useAuth();
    const navigate = useNavigate();
    const handleLogout = () => {
        sessionStorage.removeItem('token');
        setIsAuthenticated(false);
        navigate('/');
    }

    return (
        <nav className="navbar navbar-expand-lg navbar-dark">
            <div className="container-lg container-fluid">
                <Link className="navbar-brand d-flex align-items-center justify-content-center" to="/"
                      style={{width: '100px', height: '100px'}}>
                    <img src="/logo.png" alt="" width="200" height="200"
                         className="d-inline-block align-text-top"/>
                    <span style={{fontSize: '2rem'}}>Minigram</span>
                </Link>
                <div className="collapse navbar-collapse justify-content-center" id="navbarNav">
                    <ul className="navbar-nav mx-auto">
                        <li className="nav-item">
                            <Link className="nav-link" to="/">Home</Link>
                        </li>
                        {!isAuthenticated && (
                            <li className="nav-item">
                                <Link className="nav-link" to="/register">Register</Link>
                            </li>
                        )}
                    </ul>
                    {isAuthenticated && (
                        <Dropdown>
                            <Dropdown.Toggle variant="none" id="dropdown-basic">
                                <img src={profilePic || defaultProfilePic} alt="Profile" className="rounded-circle"
                                     style={{width: '40px', height: '40px'}}/>
                            </Dropdown.Toggle>

                            <Dropdown.Menu>
                                <Dropdown.Item href="/profile">Your Profile</Dropdown.Item>
                                <Dropdown.Item onClick={handleLogout}>Logout</Dropdown.Item>
                            </Dropdown.Menu>
                        </Dropdown>
                    )}
                    {!isAuthenticated && (
                        <ul className="navbar-nav ms-auto">
                            <li className="nav-item">
                                <Link className="nav-link" to="/login">Login</Link>
                            </li>
                        </ul>
                    )}
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
