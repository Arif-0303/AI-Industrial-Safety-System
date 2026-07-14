import { useState } from "react";
import axios from "axios";

function AIChat() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = {
      sender: "You",
      text: message,
    };

    setMessages((prev) => [...prev, userMessage]);

    try {
      const res = await axios.post(
        "https://ai-industrial-safety-system.onrender.com/chat/",
        {
          message,
        }
      );

      setMessages((prev) => [
        ...prev,
        {
          sender: "AI",
          text: res.data.response,
        },
      ]);

      setMessage("");
    } catch (err) {
      console.error(err);

      setMessages((prev) => [
        ...prev,
        {
          sender: "AI",
          text: "Unable to connect to AI Assistant.",
        },
      ]);
    }
  };

  return (
    <div className="max-w-5xl mx-auto p-6">

      <h1 className="text-3xl font-bold mb-6">
        AI Safety Assistant
      </h1>

      <div className="border rounded-lg h-[500px] overflow-y-auto p-4 bg-white">

        {messages.map((msg, index) => (
          <div
            key={index}
            className={`mb-4 ${
              msg.sender === "You"
                ? "text-right"
                : "text-left"
            }`}
          >
            <div
              className={`inline-block px-4 py-3 rounded-lg ${
                msg.sender === "You"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-200"
              }`}
            >
              <strong>{msg.sender}</strong>
              <br />
              {msg.text}
            </div>
          </div>
        ))}

      </div>

      <div className="flex gap-3 mt-4">

        <input
          className="flex-1 border rounded-lg px-4 py-3"
          value={message}
          placeholder="Ask about industrial safety..."
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") sendMessage();
          }}
        />

        <button
          onClick={sendMessage}
          className="bg-blue-600 text-white px-6 rounded-lg"
        >
          Send
        </button>

      </div>

    </div>
  );
}

export default AIChat;