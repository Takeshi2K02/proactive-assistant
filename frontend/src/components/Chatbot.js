import React, { useState } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

const Chatbot = () => {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');

  const sendMessage = async () => {
    try {
      const res = await axios.post('http://localhost:5000/chat', { message });
      setResponse(res.data.response); // The response is HTML or Markdown
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <h2>Chatbot</h2>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Ask something..."
      />
      <button onClick={sendMessage}>Send</button>

      <div>
        <h3>Response:</h3>
        <div className="markdown-content">
          <ReactMarkdown>{response}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;