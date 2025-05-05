import { useState, useRef, useEffect } from 'react';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Салам! Мен AITilchi. Сизге кандай жардам бере алам?",
      sender: "bot"
    }
  ]);
  const [inputMessage, setInputMessage] = useState("");
  const messagesEndRef = useRef(null);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    // Add user message
    const userMessage = {
      id: messages.length + 1,
      text: inputMessage,
      sender: "user"
    };
    setMessages(prev => [...prev, userMessage]);
    setInputMessage("");

    // Add bot response after a short delay
    setTimeout(() => {
      const botMessage = {
        id: messages.length + 2,
        text: "Салам, мен AITilchi — кыргыз тилинин грамматикасына арналган чат ботмун.",
        sender: "bot"
      };
      setMessages(prev => [...prev, botMessage]);
    }, 500);
  };

  return (
    <div className="fixed bottom-4 right-4 z-50">
      {/* Chat Icon Button - Only visible when chat is closed */}
      {!isOpen && (
        <button
          onClick={toggleChat}
          className="w-14 h-14 bg-red-700 dark:bg-red-600 text-white rounded-full shadow-lg hover:bg-red-600 dark:hover:bg-red-500 transition-colors duration-200 flex items-center justify-center focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50"
          aria-label="Open chat"
        >
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
            />
          </svg>
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed inset-0 sm:inset-auto sm:absolute sm:bottom-16 sm:right-0 
          w-screen h-screen sm:w-[400px] sm:h-[500px]
          bg-white dark:bg-[#1a1a1a] 
          rounded-none sm:rounded-lg shadow-xl flex flex-col 
          border-0 sm:border border-gray-200 dark:border-gray-800 
          transition-all duration-200
          max-h-[100vh] overflow-hidden">      
          {/* Chat Header */}
          <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-[#1a1a1a] sticky top-0 z-10">
            <h3 className="text-lg font-semibold text-black dark:text-white">
              AITilchi чат
            </h3>
            <button
              onClick={toggleChat}
              className="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50 rounded-full p-1"
              aria-label="Close chat"
            >
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>

          {/* Chat Messages Area */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex items-start space-x-2 ${
                  message.sender === "user" ? "justify-end" : ""
                }`}
              >
                {message.sender === "bot" && (
                  <div className="w-8 h-8 rounded-full bg-red-600 flex items-center justify-center text-white text-sm">
                    AI
                  </div>
                )}
                <div
                  className={`flex-1 ${
                    message.sender === "user"
                      ? "bg-red-600 text-white"
                      : "bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400"
                  } rounded-lg p-3 max-w-[80%]`}
                >
                  <p className="text-sm">{message.text}</p>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Chat Input Area */}
          <div className="p-4 border-t border-gray-200 dark:border-gray-800 bg-white dark:bg-[#1a1a1a] sticky bottom-0">
            <form onSubmit={handleSendMessage} className="flex space-x-2">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Жазгыла..."
                className="flex-1 px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-black dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent"
                aria-label="Message input"
              />
              <button
                type="submit"
                className="px-4 py-2 bg-red-700 dark:bg-red-600 text-white rounded-lg hover:bg-red-600 dark:hover:bg-red-500 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50"
                aria-label="Send message"
              >
                <svg
                  className="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                  />
                </svg>
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatWidget; 