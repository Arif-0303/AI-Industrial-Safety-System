import { useState } from "react";
import MainLayout from "../../layouts/MainLayout";
import { askAI } from "../../services/chatService";

function AIQuery() {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [chat, setChat] = useState([]);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = message;

    setChat((prev) => [
      ...prev,
      {
        sender: "You",
        text: userMessage,
      },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const res = await askAI(userMessage);

      setChat((prev) => [
        ...prev,
        {
          sender: "AI",
          text: res.response,
        },
      ]);
    } catch (err) {
      setChat((prev) => [
        ...prev,
        {
          sender: "AI",
          text: "Unable to contact AI server.",
        },
      ]);
    }

    setLoading(false);
  };

  return (
    <MainLayout>
      <div className="max-w-5xl mx-auto">

        <div className="bg-gray-900 rounded-xl p-6 shadow-lg">

          <h1 className="text-4xl font-bold text-white mb-2">
            🤖 AI Steel Plant Assistant
          </h1>

          <p className="text-gray-300 mb-6">
            Ask anything about plant safety, incidents,
            maintenance, risk score or machine health.
          </p>

          <div className="bg-gray-800 rounded-xl p-4 h-[500px] overflow-y-auto">

            {chat.length === 0 && (
              <div className="text-gray-400 text-center mt-24">
                Start a conversation with the AI Assistant
              </div>
            )}

            {chat.map((item, index) => (
              <div
                key={index}
                className={`mb-4 ${
                  item.sender === "You"
                    ? "text-right"
                    : "text-left"
                }`}
              >
                <div
                  className={`inline-block max-w-[80%] rounded-xl px-4 py-3 ${
                    item.sender === "You"
                      ? "bg-blue-600 text-white"
                      : "bg-gray-700 text-gray-100"
                  }`}
                >
                  <div className="font-bold mb-1">
                    {item.sender}
                  </div>

                  <div className="whitespace-pre-wrap">
                    {item.text}
                  </div>
                </div>
              </div>
            ))}

            {loading && (
              <div className="text-gray-300 mt-4">
                🤖 AI is thinking...
              </div>
            )}

          </div>

          <div className="flex mt-5 gap-3">

            <input
              type="text"
              value={message}
              placeholder="Ask about risk score, maintenance, incidents..."
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  sendMessage();
                }
              }}
              className="flex-1 rounded-lg border border-gray-700 bg-gray-800 text-white px-4 py-3 outline-none"
            />

            <button
              onClick={sendMessage}
              className="bg-blue-600 hover:bg-blue-700 px-6 rounded-lg text-white font-semibold"
            >
              Send
            </button>

          </div>

        </div>
      </div>
    </MainLayout>
  );
}

export default AIQuery;