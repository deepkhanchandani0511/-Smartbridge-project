import React, { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Send,
  Sparkles,
  Bot,
  User,
  Image as ImageIcon,
  Loader2,
  Copy,
  ThumbsUp,
  ThumbsDown,
} from "lucide-react";
import { chatAPI } from "../services/api";
import toast from "react-hot-toast";

const suggestions = [
  "Show photos of John",
  "Upload new photos",
  "Send photos to email",
  "Find recent photos",
  "Who is in my photos?",
];

export default function Chatbot() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm your AI photo assistant. I can help you manage, organize, and share your photos. Try asking me things like:",
      sender: "bot",
      timestamp: new Date(),
      suggestions: [
        "Show photos of John",
        "Find recent photos",
        "Send photos to email",
      ],
    },
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (message = inputValue) => {
    if (!message.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: message,
      sender: "user",
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);

    try {
      const response = await chatAPI.send(message);
      const botMessage = {
        id: Date.now() + 1,
        text: response.data.response,
        sender: "bot",
        timestamp: new Date(),
        action: response.data.action,
        data: response.data.data,
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        text: "I apologize, but I encountered an error. Please try again.",
        sender: "bot",
        timestamp: new Date(),
        isError: true,
      };
      setMessages((prev) => [...prev, errorMessage]);
      toast.error("Failed to send message");
    } finally {
      setIsLoading(false);
    }
  };

  const formatTime = (date) => {
    return new Date(date).toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <div className="h-[calc(100vh-180px)] flex flex-col -m-6">
      {/* Header */}
      <div className="card rounded-none rounded-t-2xl p-4 flex items-center justify-between border-b border-white/[0.06]">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 bg-gradient-to-br from-primary to-secondary rounded-lg flex items-center justify-center">
            <Sparkles className="w-4 h-4 text-white" />
          </div>
          <div>
            <h3 className="font-medium text-foreground text-sm">
              AI Assistant
            </h3>
            <p className="text-xs text-muted-foreground">Online</p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar">
        {messages.map((message, index) => (
          <motion.div
            key={message.id}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2 }}
            className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`flex items-end gap-2 max-w-[85%] ${message.sender === "user" ? "flex-row-reverse" : ""}`}
            >
              {/* Avatar */}
              <div
                className={`w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0 ${
                  message.sender === "user"
                    ? "bg-gradient-to-br from-primary to-secondary"
                    : "bg-white/[0.06]"
                }`}
              >
                {message.sender === "user" ? (
                  <User className="w-3.5 h-3.5 text-white" />
                ) : (
                  <Bot className="w-3.5 h-3.5 text-muted-foreground" />
                )}
              </div>

              {/* Bubble */}
              <div
                className={`flex flex-col ${message.sender === "user" ? "items-end" : "items-start"}`}
              >
                <div
                  className={`chat-bubble ${
                    message.sender === "user"
                      ? "chat-bubble-user"
                      : "chat-bubble-bot"
                  } ${message.isError ? "border-red-500/20 bg-red-500/5" : ""}`}
                >
                  <p className="text-sm leading-relaxed">{message.text}</p>
                </div>

                {/* Suggestions */}
                {message.suggestions && (
                  <div className="mt-2 flex flex-wrap gap-1.5">
                    {message.suggestions.map((suggestion, idx) => (
                      <button
                        key={idx}
                        onClick={() => handleSendMessage(suggestion)}
                        className="px-2.5 py-1 rounded-md text-xs bg-white/[0.03] text-muted-foreground hover:bg-white/[0.06] hover:text-foreground border border-white/[0.04] transition-colors"
                      >
                        {suggestion}
                      </button>
                    ))}
                  </div>
                )}

                {/* Time */}
                <span className="text-[10px] text-muted-foreground mt-1.5 px-1">
                  {formatTime(message.timestamp)}
                </span>
              </div>
            </div>
          </motion.div>
        ))}

        {/* Typing Indicator */}
        <AnimatePresence>
          {isLoading && (
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              className="flex justify-start"
            >
              <div className="flex items-end gap-2">
                <div className="w-7 h-7 rounded-full bg-white/[0.06] flex items-center justify-center">
                  <Bot className="w-3.5 h-3.5 text-muted-foreground" />
                </div>
                <div className="chat-bubble chat-bubble-bot">
                  <div className="flex gap-1">
                    {[0, 1, 2].map((i) => (
                      <motion.div
                        key={i}
                        animate={{ y: [0, -4, 0] }}
                        transition={{
                          repeat: Infinity,
                          duration: 0.6,
                          delay: i * 0.15,
                        }}
                        className="w-1.5 h-1.5 bg-muted-foreground rounded-full"
                      />
                    ))}
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Quick Suggestions (initial) */}
        {messages.length === 1 && !isLoading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="flex flex-wrap gap-2 justify-center pt-2"
          >
            <p className="w-full text-center text-xs text-muted-foreground mb-1">
              Try asking:
            </p>
            {suggestions.slice(0, 4).map((suggestion, index) => (
              <button
                key={index}
                onClick={() => handleSendMessage(suggestion)}
                className="px-3 py-1.5 rounded-lg text-xs bg-white/[0.03] text-muted-foreground hover:bg-white/[0.06] hover:text-foreground border border-white/[0.04] transition-colors"
              >
                {suggestion}
              </button>
            ))}
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t border-white/[0.06] bg-card">
        <div className="flex items-end gap-2">
          <div className="flex-1 relative">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSendMessage();
                }
              }}
              placeholder="Ask me anything..."
              className="input resize-none min-h-[44px] max-h-32 py-2.5"
              rows={1}
              disabled={isLoading}
            />
          </div>
          <button
            onClick={() => handleSendMessage()}
            disabled={isLoading || !inputValue.trim()}
            className="btn-primary p-2.5"
          >
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
