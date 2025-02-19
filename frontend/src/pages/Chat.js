import React, { useState, useEffect } from 'react';
import axios from 'axios';
import QuestionBlock from '../components/QuestionBlock';
import AnswerBlock from '../components/AnswerBlock';
import './Chat.css';

const ChatPage = () => {
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
  }, [messages]);

  const sendMessage = async () => {
    if (message.trim() === '') return;

    const userMessage = { text: message, sender: 'user' };
    setMessages(prevMessages => [...prevMessages, userMessage]);

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

  const deleteMessage = (index) => {
    setMessages(prevMessages => {
      const updatedMessages = prevMessages.filter((_, i) => i !== index && i !== index + 1);
      sessionStorage.setItem('chatMessages', JSON.stringify(updatedMessages));
      return updatedMessages;
    });
  };

  return (
    <div className="chat-container">
      <div className="chat-box">
        <div className="messages">
          {messages.map((msg, index) => (
            msg.sender === 'user' ? (
              <QuestionBlock key={index} text={msg.text} onDelete={() => deleteMessage(index)} />
            ) : (
              <AnswerBlock key={index} text={msg.text} />
            )
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
};

export default ChatPage;