import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import './Chat.css';

function Chat() {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);

  // Load messages from sessionStorage on mount
  useEffect(() => {
    const savedMessages = sessionStorage.getItem('chatMessages');
    if (savedMessages) {
      setMessages(JSON.parse(savedMessages));
    }
  }, []);

  // Save messages to sessionStorage after messages update
  useEffect(() => {
    if (messages.length > 0) {
      sessionStorage.setItem('chatMessages', JSON.stringify(messages));
    }
  }, [messages]); // Run effect when messages change

  const sendMessage = async () => {
    if (message.trim() === '') return;

    const userMessage = { text: message, sender: 'user' };
    const updatedMessages = [...messages, userMessage];

    setMessages(updatedMessages);

    try {
      const res = await axios.post('http://localhost:5000/chat', { message });
      const assistantMessage = { text: res.data.response, sender: 'assistant' };

      setMessages(prevMessages => {
        const newMessages = [...prevMessages, assistantMessage];
        sessionStorage.setItem('chatMessages', JSON.stringify(newMessages)); // Ensure session storage update
        return newMessages;
      });
    } catch (error) {
      console.error('Error:', error);
    }

    setMessage('');
  };

  return (
    <div className="chat-container">
      <div className="chat-box">
        <div className="messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.sender}-message`}>
              <ReactMarkdown>{msg.text}</ReactMarkdown>
            </div>
          ))}
        </div>

        <div className="input-area">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Ask something..."
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default Chat;