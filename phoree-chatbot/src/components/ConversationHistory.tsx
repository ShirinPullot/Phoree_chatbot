import { useEffect, useRef } from 'react';
import { Message } from '@/types/chat';

export default function ConversationHistory({ messages }: { messages: Message[] }) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="space-y-4 pb-4 px-4 max-w-3xl mx-auto">
      {messages.map((message) => (
        <div
          key={message.id}
          className={`flex items-start gap-3 ${
            message.role === 'user' ? 'flex-row-reverse' : 'flex-row'
          }`}
        >
          {/* Avatar */}
          <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center
            ${message.role === 'user' 
              ? 'bg-blue-100 text-blue-600' 
              : 'bg-emerald-100 text-emerald-600'
            }`}
          >
            {message.role === 'user' ? '👤' : '🏠'}
          </div>

          {/* Message bubble */}
          <div
            className={`rounded-2xl px-4 py-2 max-w-[80%] shadow-sm
              ${message.role === 'user'
                ? 'bg-blue-600 text-white'
                : 'bg-white border border-gray-200 text-gray-800'
              }`}
          >
            <p className="whitespace-pre-wrap text-sm leading-relaxed">
              {message.content}
            </p>
          </div>
        </div>
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
}

