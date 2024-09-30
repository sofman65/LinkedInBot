import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Post {
    id: number;
    text: string;
}

const ApprovalDashboard: React.FC = () => {
    const [pendingPosts, setPendingPosts] = useState<Post[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Fetch pending posts from the backend
        const fetchPendingPosts = async () => {
            try {
                const response = await axios.get('/api/pending-posts/');
                setPendingPosts(response.data);
                setLoading(false);
            } catch (error) {
                console.error('Error fetching pending posts:', error);
                setLoading(false);
            }
        };

        fetchPendingPosts();
    }, []);

    // Approve a post
    const approvePost = async (postId: number) => {
        try {
            await axios.post(`/api/approve-post/${postId}/`);
            alert('Post approved!');
            setPendingPosts(pendingPosts.filter(post => post.id !== postId));
        } catch (error) {
            console.error('Error approving post:', error);
        }
    };

    // Reject a post
    const rejectPost = async (postId: number) => {
        try {
            await axios.post(`/api/reject-post/${postId}/`);
            alert('Post rejected!');
            setPendingPosts(pendingPosts.filter(post => post.id !== postId));
        } catch (error) {
            console.error('Error rejecting post:', error);
        }
    };

    if (loading) {
        return <p>Loading pending posts...</p>;
    }

    return (
        <div>
            <h1>Pending Post Approvals</h1>
            <ul>
                {pendingPosts.map(post => (
                    <li key={post.id}>
                        <p>{post.text}</p>
                        <button onClick={() => approvePost(post.id)}>Approve</button>
                        <button onClick={() => rejectPost(post.id)}>Reject</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ApprovalDashboard;
