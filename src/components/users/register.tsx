import React, {useState} from 'react';
import axios from 'axios';
import {useNavigate} from 'react-router-dom';

interface RegisterErrors {
    username?: string;
    firstName?: string;
    lastName?: string;
    email?: string;
    password1?: string;
    password2?: string;
}

const Register: React.FC = () => {
    const [formData, setFormData] = useState({
        username: '',
        first_name: '',
        last_name: '',
        email: '',
        password1: '',
        password2: '',
    });
    const [errors, setErrors] = useState<RegisterErrors>({});
    const navigate = useNavigate();

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const {name, value} = e.target;
        const adjustedName = name === 'firstName' ? 'first_name' : name === 'lastName' ? 'last_name' : name;
        setFormData({...formData, [e.target.name]: e.target.value});
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        // Simple client-side validation for example purposes
        if (formData.password1 !== formData.password2) {
            setErrors({...errors, password2: 'Passwords do not match'});
            return;
        }

        try {
            // Adjust the URL to your API endpoint
            const response = await axios.post('http://localhost:8000/api/register/', formData);
            console.log(response.data);
            // Redirect on successful registration
            navigate('/login');
        } catch (error) {
            if (axios.isAxiosError(error) && error.response) {
                // Handle errors (adjust according to your API response structure)
                setErrors(error.response.data.errors);
            }
        }
    };

    return (
        <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-md-6">
                    <div className="card" style={{backgroundColor: "#FBFADA"}}>
                        <div className="card-header text-center">
                            <h2>Register</h2>
                        </div>
                        <div className="card-body">
                            <form className="p-4" onSubmit={handleSubmit}>

                                <div className="mb-3">
                                    <label htmlFor="username" className="form-label">Username</label>
                                    <input
                                        type="text"
                                        className={`form-control ${errors.username ? 'is-invalid' : ''}`}
                                        id="username"
                                        name="username"
                                        value={formData.username}
                                        onChange={handleChange}
                                        required
                                    />
                                    {errors.username && <div className="invalid-feedback">{errors.username}</div>}
                                </div>

                                <div className="row">
                                    <div className="col-6 mb-3">
                                        <label htmlFor="firstname" className="form-label">Firstname</label>
                                        <input
                                            type="text"
                                            className={`form-control ${errors.firstName ? 'is-invalid' : ''}`}
                                            id="firstname"
                                            name="first_name"
                                            value={formData.first_name}
                                            onChange={handleChange}
                                            required
                                        />
                                        {errors.firstName && <div className="invalid-feedback">{errors.firstName}</div>}
                                    </div>
                                    <div className="col-6 mb-3">
                                        <label htmlFor="lastname" className="form-label">Lastname</label>
                                        <input
                                            type="text"
                                            className={`form-control ${errors.lastName ? 'is-invalid' : ''}`}
                                            id="lastname"
                                            name="last_name"
                                            value={formData.last_name}
                                            onChange={handleChange}
                                            required
                                        />
                                        {errors.lastName && <div className="invalid-feedback">{errors.lastName}</div>}
                                    </div>
                                </div>


                                <div className="mb-3">
                                    <label htmlFor="email" className="form-label">Email</label>
                                    <input
                                        type="email"
                                        className={`form-control ${errors.email ? 'is-invalid' : ''}`}
                                        id="email"
                                        name="email"
                                        value={formData.email}
                                        onChange={handleChange}
                                        required
                                    />
                                    {errors.email && <div className="invalid-feedback">{errors.email}</div>}
                                </div>

                                <div className="mb-3">
                                    <label htmlFor="password1" className="form-label">Password</label>
                                    <input
                                        type="password"
                                        className={`form-control ${errors.password1 ? 'is-invalid' : ''}`}
                                        id="password1"
                                        name="password1"
                                        value={formData.password1}
                                        onChange={handleChange}
                                        required
                                    />
                                    {errors.password1 && <div className="invalid-feedback">{errors.password1}</div>}
                                </div>

                                <div className="mb-3">
                                    <label htmlFor="password2" className="form-label">Confirm Password</label>
                                    <input
                                        type="password"
                                        className={`form-control ${errors.password2 ? 'is-invalid' : ''}`}
                                        id="password2"
                                        name="password2"
                                        value={formData.password2}
                                        onChange={handleChange}
                                        required
                                    />
                                    {errors.password2 && <div className="invalid-feedback">{errors.password2}</div>}
                                </div>

                                <div className="mb-3 form-check">
                                    <input type="checkbox" className="form-check-input" id="exampleCheck1" required/>
                                    <label className="form-check-label" htmlFor="exampleCheck1">I agree to the terms and
                                        conditions</label>
                                </div>

                                <button type="submit" className="btn btn-success d-flex m-auto">Sign Up</button>
                            </form>
                            <p className="mt-3 text-center">Already have an account? <a href="/Login">Login</a></p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Register;
