// PostGenerator.js (React component)

import React, { useState } from 'react';
import axios from 'axios';

const PostGenerator = () => {
    const [prompt, setPrompt] = useState('');
    const [generatedPost, setGeneratedPost] = useState('');

    const handleGeneratePost = async () => {
        try {
            const response = await axios.post('http://localhost:8000/api/generate-linkedin-post/', { prompt });
            setGeneratedPost(response.data.post_content);
        } catch (error) {
            console.error('Error generating post:', error);
        }
    };

    return (
        <div>
            <h1>Generate LinkedIn Post</h1>
            <input
                type="text"
                placeholder="Enter prompt for AI"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
            />
            <button onClick={handleGeneratePost}>Generate Post</button>

            {generatedPost && (
                <div>
                    <h2>Generated Post:</h2>
                    <p>{generatedPost}</p>
                </div>
            )}
        </div>
    );
};

export default PostGenerator;
