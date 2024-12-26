'use client'

import { useState, FormEvent } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import ConversationHistory from '@/components/ConversationHistory'
import { Send, Loader2 } from 'lucide-react'

type Message = {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([{
    id: crypto.randomUUID(),
    role: 'assistant',
    content: "👋 Welcome to Phoree Real Estate! Im your personal property assistant for Dubai. How can I help you today?\n\n• Looking to buy a property?\n• Interested in renting?\n• Want to explore specific areas?\n• Need market insights?"
  }]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: input
    };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const eventSource = new EventSource(`${apiUrl}/api/chat/stream?message=${encodeURIComponent(input)}`);
      let assistantMessage = '';

      eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.content) {
          assistantMessage += data.content;
          setMessages(prev => {
            const newMessages = [...prev];
            const lastMessage = newMessages[newMessages.length - 1];
            if (lastMessage.role === 'assistant') {
              lastMessage.content = assistantMessage;
            } else {
              newMessages.push({
                id: crypto.randomUUID(),
                role: 'assistant',
                content: assistantMessage
              });
            }
            return newMessages;
          });
        }
      };

      eventSource.onerror = (error) => {
        console.error('SSE Error:', error);
        eventSource.close();
        setIsLoading(false);
      };

      eventSource.addEventListener('done', () => {
        eventSource.close();
        setIsLoading(false);
      });
    } catch (error) {
      console.error('Chat error:', error);
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <span className="text-2xl font-bold text-emerald-600">🏠 Phoree</span>
              <span className="ml-2 text-sm text-gray-500">Real Estate Assistant</span>
            </div>
            <div className="text-sm text-gray-500">Dubai Premier Property Guide</div>
            </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Card className="min-h-[80vh] flex flex-col bg-white/80 backdrop-blur-sm shadow-xl">
          <CardHeader className="border-b border-gray-100 bg-white">
            <CardTitle className="text-lg font-medium text-gray-900">
              Chat with our AI Property Expert
            </CardTitle>
          </CardHeader>
          
          <CardContent className="flex-1 overflow-y-auto p-6 scroll-smooth">
            <ConversationHistory messages={messages} />
          </CardContent>

          <CardFooter className="border-t border-gray-100 bg-white p-4">
            <form onSubmit={handleSubmit} className="flex w-full space-x-2">
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about properties in Dubai..."
                className="flex-1 bg-gray-50 border-gray-200 focus:border-emerald-500 focus:ring-emerald-500"
                disabled={isLoading}
              />
              <Button 
                type="submit" 
                disabled={isLoading}
                className="bg-emerald-600 hover:bg-emerald-700 text-white"
              >
                {isLoading ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <Send className="h-4 w-4" />
                )}
              </Button>
            </form>
          </CardFooter>
        </Card>
      </main>
    </div>
  )
}

