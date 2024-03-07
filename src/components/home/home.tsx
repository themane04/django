import React, {useEffect, useState, useContext} from 'react';
import {useNavigate} from 'react-router-dom';
import {Modal, Button, Alert} from 'react-bootstrap';
import {useAuth} from '../users/auth';
import axios from 'axios';
import PostComponent from './posts';

interface Author {
    username: string;
    profile_pic?: string;
}

interface Post {
    id: number;
    title: string;
    content: string;
    image: { url: string; } | null;
    author: {
        username: string;
        profile: {
            profile_pic: { url: string; } | null;
        };
    };
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

    useEffect(() => {
        const fetchPosts = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/posts', {
                    headers: {
                        'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
                    },
                });
                setPosts(response.data);
            } catch (error) {
                console.error('Error fetching posts:', error);
                // Optionally, handle errors, e.g., by setting an error message state
            }
        };

        fetchPosts();
    }, []); // Empty dependency array means this effect runs once on component mount


    return (
        <>
            <div className="container">
                <div className="text-center">
                    {messages.map((message, index) => (
                        <Alert key={index} variant="success" dismissible>
                            {message}
                        </Alert>
                    ))}
                </div>

                {/*The Post Form Start*/}
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
            </div>
            {/*The Post Form End*/}

            {/*The Post List Start*/}
            <PostComponent posts={posts}/>
            {/*The Post List End*/}

        </>
    );
};

export default Home;
