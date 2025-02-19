import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane } from '@fortawesome/free-solid-svg-icons';
import QuestionBlock from '../components/QuestionBlock';
import AnswerBlock from '../components/AnswerBlock';
import './Chat.css';

const ChatPage = () => {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const textAreaRef = useRef(null);

  useEffect(() => {
    const savedMessages = sessionStorage.getItem('chatMessages');
    if (savedMessages) {
      setMessages(JSON.parse(savedMessages));
    }
  }, []);

  useEffect(() => {
    if (messages.length > 0) {
      sessionStorage.setItem('chatMessages', JSON.stringify(messages));
    }
  }, [messages]);

  useEffect(() => {
    if (textAreaRef.current) {
      textAreaRef.current.style.height = 'auto';
      textAreaRef.current.style.height = textAreaRef.current.scrollHeight + 'px';
    }
  }, [message]);

  const sendMessage = async () => {
    if (message.trim() === '') return;

    const userMessage = { text: message, sender: 'user' };
    setMessages(prevMessages => [...prevMessages, userMessage]);

    try {
      const res = await axios.post('http://localhost:5000/chat', { message });
      const assistantMessage = { text: res.data.response, sender: 'assistant' };

      setMessages(prevMessages => {
        const newMessages = [...prevMessages, assistantMessage];
        sessionStorage.setItem('chatMessages', JSON.stringify(newMessages));
        return newMessages;
      });
    } catch (error) {
      console.error('Error:', error);
    }

    setMessage('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-box">
        <div className="messages">
          {messages.map((msg, index) => (
            msg.sender === 'user' ? (
              <QuestionBlock key={index} text={msg.text} />
            ) : (
              <AnswerBlock key={index} text={msg.text} />
            )
          ))}
        </div>

        <div className="input-area">
          <div className="input-wrapper"> {/* Added Wrapper */}
            <textarea
              ref={textAreaRef}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Ask something..."
              onKeyDown={handleKeyDown}
              rows={1}
              style={{ overflowY: 'hidden', resize: 'none' }}
            />
            <button className="inside-button" onClick={sendMessage}>
              <FontAwesomeIcon icon={faPaperPlane} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;