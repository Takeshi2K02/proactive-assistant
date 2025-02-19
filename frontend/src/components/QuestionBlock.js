import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Trash2 } from 'lucide-react'; // Import the trash icon

const QuestionBlock = ({ text, onDelete }) => {
  return (
    <div className="message-container">
      <button className="delete-button" onClick={onDelete}>
        <Trash2 size={16} color="#ff4d4d" />
      </button>
      <div className="message user-message">
        <ReactMarkdown>{text}</ReactMarkdown>
      </div>
    </div>
  );
};

export default QuestionBlock;