import { useState } from "react";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hey. I'm AgentFlow. I can search the web, send emails, and manage your Google Calendar.",
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    const message = input.trim();

    if (!message || loading) return;

    setMessages((prev) => [...prev, { role: "user", content: message }]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            typeof data.response === "string"
              ? data.response
              : JSON.stringify(data.response),
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Couldn't reach AgentFlow. Make sure the backend is running.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark">A</div>
          <div>
            <div className="brand-name">AgentFlow</div>
            <div className="status">
              <span className="status-dot"></span>
              Ready
            </div>
          </div>
        </div>

        <div className="tools">
          <span>Web</span>
          <span>Gmail</span>
          <span>Calendar</span>
        </div>
      </header>

      <main className="chat-container">
        <div className="messages">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message-row ${
                message.role === "user" ? "user-row" : "assistant-row"
              }`}
            >
              {message.role === "assistant" && (
                <div className="avatar">A</div>
              )}

              <div
                className={`message ${
                  message.role === "user"
                    ? "user-message"
                    : "assistant-message"
                }`}
              >
                {message.content}
              </div>
            </div>
          ))}

          {loading && (
            <div className="message-row assistant-row">
              <div className="avatar">A</div>
              <div className="assistant-message typing">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}
        </div>

        <div className="composer-wrap">
          <div className="composer">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask AgentFlow to do something..."
              rows="1"
            />

            <button onClick={sendMessage} disabled={!input.trim() || loading}>
              ↑
            </button>
          </div>

          <p className="hint">
            Try: “Find the latest AI news and email me a summary.”
          </p>
        </div>
      </main>
    </div>
  );
}

export default App;