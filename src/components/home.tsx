import React, {useEffect, useState, useContext} from 'react';
import {useNavigate} from 'react-router-dom';
import {Modal, Button, Alert} from 'react-bootstrap';
import {useAuth} from './users/auth'; // Adjust the import path
import axios from 'axios';

interface Author {
    username: string;
    profile_pic?: string;
}

interface Post {
    id: number;
    title: string;
    content: string;
    author: Author;
    image?: string;
}


const Home: React.FC = () => {
    const [posts, setPosts] = useState<Post[]>([]);
    const [messages, setMessages] = useState<string[]>([]);
    const {isAuthenticated} = useAuth();
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [image, setImage] = useState<File | null>(null);
    const navigate = useNavigate();
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault(); // Prevent default form submission

        const formData = new FormData();
        formData.append('title', title);
        formData.append('content', content);
        // if (image) formData.append('image', image);
        console.log(formData.get('content'));

        try {
            // Adjust the URL to your API endpoint for creating a post
            console.log(sessionStorage.getItem('token'));

            const response = await axios.post('http://localhost:8000/api/posts', formData, {
                headers: {
                    'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
                    'Content-Type': 'multipart/form-data',
                },
            });
            // Handle response...
            console.log(response.data);
        } catch (error) {
            console.error('Error creating post:', error);
        }
    };

    axios.interceptors.response.use(response => response, async error => {
        const originalRequest = error.config;
        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            try {
                const {data} = await axios.post('http://localhost:8000/api/token/refresh/', {
                    refresh: sessionStorage.getItem('refresh_token'), // Assuming you store the refresh token
                });
                sessionStorage.setItem('token', data.access); // Update the access token
                axios.defaults.headers.common['Authorization'] = `Bearer ${data.access}`; // Update the default token
                return axios(originalRequest); // Retry the original request with the new token
            } catch (refreshError) {
                console.error('Error refreshing token:', refreshError);
                // Handle token refresh error, e.g., clear session and redirect to log in
                return Promise.reject(refreshError);
            }
        }
        return Promise.reject(error);
    });

    return (
        <div className="container">
            <div className="text-center">
                {messages.map((message, index) => (
                    <Alert key={index} variant="success" dismissible>
                        {message}
                    </Alert>
                ))}
            </div>

            {isAuthenticated && (
                <div className="body-create-post">
                    <div className="container mt-5">
                        <div className="row justify-content-center">
                            <div className="col-md-6">
                                <div className="form-create-post">
                                    <h1 className="text-center">Create New Post</h1>
                                    <form method="post" className="m-3" onSubmit={handleSubmit}
                                          encType="multipart/form-data">
                                        <div className="form-group mt-2">
                                            <input
                                                type="text"
                                                className="form-control"
                                                id="title"
                                                name="title"
                                                placeholder="Enter title"
                                                required
                                                value={title}
                                                onChange={(e) => setTitle(e.target.value)}
                                            />
                                        </div>
                                        <div className="form-group mt-2">
                                    <textarea
                                        className="form-control"
                                        id="content"
                                        name="content"
                                        rows={5}
                                        placeholder="What is on your mind..."
                                        required
                                        value={content}
                                        onChange={(e) => setContent(e.target.value)}
                                    />
                                        </div>
                                        <div className="form-group mt-2">
                                            <input
                                                type="file"
                                                className="form-control"
                                                id="image"
                                                name="image"
                                                onChange={(e) => setImage(e.target.files ? e.target.files[0] : null)}
                                            />
                                        </div>
                                        <div className="text-center mt-2">
                                            <button type="submit" className="btn btn-light">
                                                <i className="fas fa-paper-plane"></i> Publish
                                            </button>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            <div className="row mt-5">
                {posts.map((post) => (
                    <div key={post.id} className="col-md-4">
                        <div className="card">
                            <div className="card-header">
                                <h5>{post.title}</h5>
                            </div>
                            <div className="card-body">
                                <p>{post.content}</p>
                                <p>Author: {post.author.username}</p>
                                {post.image && (
                                    <img src={post.image} alt="Post" className="img-fluid"/>
                                )}
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Home;
