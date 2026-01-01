import React, { useState, useEffect, useRef } from 'react'
import styled from 'styled-components'
import { chatService } from '../services/chatService'
import MessageList from './MessageList'
import MessageInput from './MessageInput'
import LanguageSelector from './LanguageSelector'
import { useAuth } from '../context/AuthContext'
import { translations } from '../translations'

const ChatContainer = styled.div.attrs(props => ({
  className: props.$isRTL ? 'rtl' : 'ltr'
}))`
  display: flex;
  height: 100vh;
  background: #f5f5f5;
  width: 100%;
`

const ChatMain = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
`

const ChatHeader = styled.div`
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
`

const Title = styled.h1`
  font-size: 1.5rem;
  margin: 0;
`

const HeaderRight = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
`

const LogoutButton = styled.button`
  padding: 0.5rem 1rem;
  background: rgba(255,255,255,0.2);
  color: white;
  border: 1px solid rgba(255,255,255,0.3);
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;
  
  &:hover {
    background: rgba(255,255,255,0.3);
  }
`

const MessagesArea = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
`

const LoadingIndicator = styled.div`
  padding: 1rem;
  text-align: center;
  color: #666;
  font-style: italic;
`

function ChatInterface({ conversationId, onConversationChange, language, onLanguageUpdate }) {
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [currentConversationId, setCurrentConversationId] = useState(conversationId)
  const { user, logout } = useAuth()
  const messagesEndRef = useRef(null)

  useEffect(() => {
    setCurrentConversationId(conversationId)
    if (conversationId) {
      loadConversation(conversationId)
    } else {
      setMessages([])
    }
  }, [conversationId])

  useEffect(() => {
    if (user?.preferred_language) {
      onLanguageUpdate(user.preferred_language)
    }
  }, [user])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const loadConversation = async (convId) => {
    try {
      const data = await chatService.getConversation(convId)
      setMessages(data.messages || [])
      if (data.conversation?.language) {
        onLanguageUpdate(data.conversation.language)
      }
    } catch (error) {
      console.error('Error loading conversation:', error)
    }
  }

  const handleSendMessage = async (messageText) => {
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: messageText,
      created_at: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setLoading(true)

    try {
      const response = await chatService.sendMessage(
        messageText,
        currentConversationId,
        language
      )

      const assistantMessage = {
        id: response.conversation_id + Date.now(),
        role: 'assistant',
        content: response.response,
        metadata: { sources: response.sources },
        created_at: new Date().toISOString()
      }

      setMessages(prev => [...prev, assistantMessage])

      if (!currentConversationId || currentConversationId !== response.conversation_id) {
        setCurrentConversationId(response.conversation_id)
        if (onConversationChange) {
          onConversationChange(response.conversation_id)
        }
      }
    } catch (error) {
      console.error('Error sending message:', error)
      const t = translations[language] || translations.fr
      const errorMessage = {
        id: Date.now(),
        role: 'assistant',
        content: t.error,
        error: true,
        created_at: new Date().toISOString()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleLanguageChange = (newLanguage) => {
    onLanguageUpdate(newLanguage)
  }

  const t = translations[language] || translations.fr
  const isRTL = language === 'ar' || language === 'am'

  return (
    <ChatContainer $isRTL={isRTL}>
      <ChatMain>
        <ChatHeader>
          <Title>{t.app_title}</Title>
          <HeaderRight>
            <LanguageSelector
              currentLanguage={language}
              onLanguageChange={handleLanguageChange}
            />
            <LogoutButton onClick={logout}>
              {t.logout}
            </LogoutButton>
          </HeaderRight>
        </ChatHeader>
        <MessagesArea>
          {messages.length === 0 && !loading && (
            <div style={{ textAlign: 'center', padding: '2rem', color: '#666' }}>
              <h2>{t.welcome_title}</h2>
              <p>{t.welcome_subtitle}</p>
              <p style={{ fontSize: '0.9rem', marginTop: '1rem' }}>
                {t.welcome_examples}
              </p>
            </div>
          )}
          <MessageList messages={messages} language={language} />
          {loading && <LoadingIndicator>{t.thinking}</LoadingIndicator>}
          <div ref={messagesEndRef} />
        </MessagesArea>
        <MessageInput
          onSendMessage={handleSendMessage}
          disabled={loading}
          language={language}
        />
      </ChatMain>
    </ChatContainer>
  )
}

export default ChatInterface

