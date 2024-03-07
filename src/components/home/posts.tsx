import React from 'react';
import {Modal} from 'react-bootstrap';

// Define the structure of the author's profile
interface Profile {
    profile_pic: {
        url: string;
    } | null;
}

// Define the structure of the author
interface Author {
    username: string;
    profile: Profile;
}

// Define the structure of a post
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

// Props for the PostsComponent
interface PostsComponentProps {
    posts: Post[];
}

const PostsComponent: React.FC<PostsComponentProps> = ({posts}) => {
    // State to handle modal visibility
    const [modalShow, setModalShow] = React.useState(false);
    const [selectedImage, setSelectedImage] = React.useState('');

    const handleShow = (imageUrl: string) => {
        setSelectedImage(imageUrl);
        setModalShow(true);
    };

    return (
        <div className="container mt-5">
            {posts.map((post) => (
                <div className="m-5" key={post.id}>
                    <div className="card" style={{backgroundColor: '#ADBC9F'}}>
                        <div className="card-body">
                            <h6 className="card-subtitle mb-2 text-muted">
                                <a style={{color: 'black'}} className="text-decoration-none"
                                   href={`/user/${post.author.username}`}>
                                    <div className="d-inline" style={{paddingLeft: '1%'}}>
                                        {post.author.username}
                                    </div>
                                </a>
                            </h6>
                            <h5 className="card-title">{post.title}</h5>
                            <p className="card-text">{post.content}</p>

                            {post.image && (
                                <>
                                    <div className="post-image pb-3" onClick={() => handleShow(post.image!.url)}>
                                        <img src={post.image.url} alt={post.title}
                                             style={{maxWidth: '50%', cursor: 'pointer'}}/>
                                    </div>
                                </>
                            )}
                        </div>
                    </div>
                </div>
            ))}

            <Modal show={modalShow} onHide={() => setModalShow(false)} centered size="lg">
                <Modal.Header closeButton/>
                <Modal.Body>
                    <img src={selectedImage} alt="Selected Post" style={{width: '100%'}}/>
                </Modal.Body>
            </Modal>
        </div>
    );
}

export default PostsComponent;
