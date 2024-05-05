import React, { useState, useRef } from 'react';
import './App.css';
import {marked} from 'marked';

const first_message = marked("Welcome to our Customer Experience Improvement Chatbot! 🤖 \n\nOur chatbot is here to enhance your customer experience by analyzing GitHub issues and providing insights from our team. Simply provide a unique GitHub issue ID from our dataframe (e.g. 437102664), and our team will promptly address it, offering valuable insights.\n\nPlease bear in mind that this process may take approximately 5-7 minutes as we work diligently to ensure the best results for you.")

function App() {
  const [messages, setMessages] = useState([
    { text: first_message, user: 'AInfineon' }
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const inputRef = useRef(null); // Create ref for the input field

  const handleSubmit = () => {
    if (isLoading) return;
    if (inputText.trim() === '') return;

    setIsLoading(true);
    //setMessages([...messages, { text: inputText, user: 'User' }]);
    setMessages(prevMessages => [
            ...prevMessages,
            { text: inputText, user: 'User' }
          ]);
    setInputText('');

    // Introduce a 2-second delay
    setTimeout(() => {
      // Make API call to send user message to local API
      fetch('http://localhost:5000/analyze_issue', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_message: inputText }),
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to send message to API');
          }
          return response.json(); // Parse response JSON
        })
        .then(data => {
          setIsLoading(false);
          if (data.errorFound == "true") {
            setIsLoading(false);
            const errorMessage = `Error: ${data.message}`;
            setMessages(prevMessages => [
              ...prevMessages,
              //{ text: inputText, user: 'User' },
              { text: errorMessage, user: 'AInfineon', isError: true}
            ]);
          }
          else {
            const chatbot_message = marked(data.chatbot_message);
            setMessages(prevMessages => [
              ...prevMessages,
              //{ text: inputText, user: 'User' },
              { text: chatbot_message, user: 'AInfineon' }
            ]);
          }
          inputRef.current.focus(); // Focus back on the input field
          
        })
        .catch(error => {
          setIsLoading(false);
          const errorMessage = `Error: ${error.message}`;
          setMessages([...messages, { text: errorMessage, user: 'AInfineon', isError: true }]);
          inputRef.current.focus(); // Focus back on the input field
        });
      }, 1500); // 1000 milliseconds = 1 seconds
  };

  const handleInputChange = event => {
    setInputText(event.target.value);
  };

  const handleKeyPress = event => {
    if (event.key === 'Enter') {
      handleSubmit();
    }
  };

  return (
    <div className="App">
      <h1>Welcome to AInfineon</h1>
      <div className="chat-container">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.isError ? 'error' : ''}`}>
            <div className="message-user">{message.user}</div>
            <div className="message-text" dangerouslySetInnerHTML={{__html: message.text}}></div>
          </div>
        ))}
      </div>
      <div className="input-container">
        <input
          type="text"
          placeholder="Type your message here..."
          value={inputText}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          //disabled={isLoading}
          ref={inputRef} 
        />
        <button onClick={handleSubmit} disabled={isLoading} className={isLoading ? 'loading' : ''}>
          {isLoading ? '...' : 'Send'}
        </button>
      </div>
      <div className="disclaimer">
        <small>The software has the potential to err, so it's wise to verify crucial details.</small>
      </div>
    </div>
  );
}

export default App;
