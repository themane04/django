import React from 'react';
import {Link} from 'react-router-dom';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faBell} from '@fortawesome/free-solid-svg-icons';

interface NavbarProps {
    isAuthenticated?: boolean;
    username?: string;
    profilePic?: string;
}

const Navbar: React.FC<NavbarProps> = ({isAuthenticated = false, username, profilePic}) => {
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
                        <ul className="navbar-nav align-items-center ms-auto">
                            <li className="nav-item dropdown">
                                <Link className="nav-link dropdown-toggle" to="#" role="button"
                                      data-bs-toggle="dropdown" aria-expanded="false">
                                    {profilePic ? (
                                        <img src={profilePic} alt="Profile" className="rounded-circle"
                                             style={{width: '40px', height: '40px'}}/>
                                    ) : (
                                        <FontAwesomeIcon icon={faBell}/>
                                    )}
                                </Link>
                                <ul className="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                                    <li><Link className="dropdown-item" to="/logout">Logout</Link></li>
                                    <li><Link className="dropdown-item" to="/profile">Your Profile</Link></li>
                                </ul>
                            </li>
                        </ul>
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
