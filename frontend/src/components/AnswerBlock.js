import React from 'react';
import ReactMarkdown from 'react-markdown';

const AnswerBlock = ({ text }) => {
  return (
    <div className="message assistant-message">
      <ReactMarkdown>{text}</ReactMarkdown>
    </div>
  );
};

export default AnswerBlock;