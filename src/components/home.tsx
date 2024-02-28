import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

// Assuming you have a type for posts
interface Post {
    id: number;
    title: string;
    content: string;
    author: { username: string; profile_pic?: string };
    image?: string;
}

const Home: React.FC = () => {
    const navigate = useNavigate();
    const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
    const [posts, setPosts] = useState<Post[]>([]);

    useEffect(() => {
        // Check if the user is authenticated
        // This is a placeholder; implement your own logic here
        const token = localStorage.getItem('token');
        setIsAuthenticated(!!token);

        // If not authenticated, redirect to login
        if (!token) {
            navigate('/login');
        }

        // Fetch posts if authenticated
        // Placeholder: replace with your actual fetch call
        if (isAuthenticated) {
            // Fetch posts logic here
        }
    }, [navigate, isAuthenticated]);

    return (
        <div>
            {isAuthenticated && (
                <div>
                    {/* Your post creation form and posts list here */}
                    <h2>Welcome to the homepage!</h2>
                    {/* Map through posts and display them */}
                </div>
            )}
        </div>
    );
};

export default Home;
