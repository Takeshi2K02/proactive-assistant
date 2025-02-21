import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faStop } from '@fortawesome/free-solid-svg-icons';

// Function to remove Markdown syntax
const stripMarkdown = (markdown) => {
  return markdown
    .replace(/\*\*(.*?)\*\*/g, '$1') // Bold (**text**)
    .replace(/\*(.*?)\*/g, '$1') // Italics (*text*)
    .replace(/__(.*?)__/g, '$1') // Bold (__text__)
    .replace(/_(.*?)_/g, '$1') // Italics (_text_)
    .replace(/\[(.*?)\]\(.*?\)/g, '$1') // Links [text](url)
    .replace(/#+\s?(.*)/g, '$1') // Headers (# Header)
    .replace(/`{1,3}([^`]+)`{1,3}/g, '$1') // Inline code
    .replace(/!\[.*?\]\(.*?\)/g, '') // Images ![alt](url)
    .replace(/>\s?(.*)/g, '$1'); // Blockquotes (> text)
};

const AnswerBlock = ({ text }) => {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [googleUSVoice, setGoogleUSVoice] = useState(null);

  useEffect(() => {
    const loadVoices = () => {
      const availableVoices = window.speechSynthesis.getVoices();
      const googleVoice = availableVoices.find(
        (voice) => voice.lang === 'en-US' && voice.name.includes('Google')
      );
      setGoogleUSVoice(googleVoice || null);
    };

    window.speechSynthesis.onvoiceschanged = loadVoices;
    loadVoices();

    return () => {
      window.speechSynthesis.onvoiceschanged = null;
    };
  }, []);

  const speak = () => {
    if (isSpeaking && !isPaused) {
      window.speechSynthesis.pause();
      setIsPaused(true);
      return;
    }

    if (isSpeaking && isPaused) {
      window.speechSynthesis.resume();
      setIsPaused(false);
      return;
    }

    if (!googleUSVoice) {
      console.error('Google US English (en-US) voice not found.');
      return;
    }

    const plainText = stripMarkdown(text); // Remove Markdown formatting
    const textChunks = plainText.match(/(.|[\r\n]){1,100}/g) || [];

    const speakChunk = (index) => {
      if (index >= textChunks.length) {
        setIsSpeaking(false);
        setIsPaused(false);
        return;
      }

      const utterance = new SpeechSynthesisUtterance(textChunks[index]);
      utterance.voice = googleUSVoice;

      utterance.onend = () => {
        speakChunk(index + 1);
      };

      window.speechSynthesis.speak(utterance);
      setIsSpeaking(true);
    };

    speakChunk(0);
  };

  const stop = () => {
    window.speechSynthesis.cancel();
    setIsSpeaking(false);
    setIsPaused(false);
  };

  return (
    <div className="message answer-container">
      <div className='assistant-message'>
        <ReactMarkdown>{text}</ReactMarkdown>
      </div>
      <div className="tts-controls" style={{ paddingLeft: '5px' }}>
        <button style={{ padding: '0px' }} onClick={speak} className="flex h-[30px] w-[30px] items-center justify-center">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="icon-md-heavy">
            <path fillRule="evenodd" clipRule="evenodd" d="M11 4.9099C11 4.47485 10.4828 4.24734 10.1621 4.54132L6.67572 7.7372C6.49129 7.90626 6.25019 8.00005 6 8.00005H4C3.44772 8.00005 3 8.44776 3 9.00005V15C3 15.5523 3.44772 16 4 16H6C6.25019 16 6.49129 16.0938 6.67572 16.2629L10.1621 19.4588C10.4828 19.7527 11 19.5252 11 19.0902V4.9099ZM8.81069 3.06701C10.4142 1.59714 13 2.73463 13 4.9099V19.0902C13 21.2655 10.4142 22.403 8.81069 20.9331L5.61102 18H4C2.34315 18 1 16.6569 1 15V9.00005C1 7.34319 2.34315 6.00005 4 6.00005H5.61102L8.81069 3.06701ZM20.3166 6.35665C20.8019 6.09313 21.409 6.27296 21.6725 6.75833C22.5191 8.3176 22.9996 10.1042 22.9996 12.0001C22.9996 13.8507 22.5418 15.5974 21.7323 17.1302C21.4744 17.6185 20.8695 17.8054 20.3811 17.5475C19.8927 17.2896 19.7059 16.6846 19.9638 16.1962C20.6249 14.9444 20.9996 13.5175 20.9996 12.0001C20.9996 10.4458 20.6064 8.98627 19.9149 7.71262C19.6514 7.22726 19.8312 6.62017 20.3166 6.35665ZM15.7994 7.90049C16.241 7.5688 16.8679 7.65789 17.1995 8.09947C18.0156 9.18593 18.4996 10.5379 18.4996 12.0001C18.4996 13.3127 18.1094 14.5372 17.4385 15.5604C17.1357 16.0222 16.5158 16.1511 16.0539 15.8483C15.5921 15.5455 15.4632 14.9255 15.766 14.4637C16.2298 13.7564 16.4996 12.9113 16.4996 12.0001C16.4996 10.9859 16.1653 10.0526 15.6004 9.30063C15.2687 8.85905 15.3578 8.23218 15.7994 7.90049Z" fill="currentColor"></path>
          </svg>
        </button>
        <button onClick={stop} disabled={!isSpeaking}>
          <FontAwesomeIcon icon={faStop} />
        </button>
      </div>
    </div>
  );
};

export default AnswerBlock;