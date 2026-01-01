import React from 'react'
import styled from 'styled-components'
import { translations } from '../translations'

const MessageContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem 0;
`

const Message = styled.div`
  display: flex;
  justify-content: ${props => props.role === 'user' ? 'flex-end' : 'flex-start'};
  animation: fadeIn 0.3s;
  
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
`

const MessageBubble = styled.div`
  max-width: 95%;
  padding: 1rem 1.25rem;
  border-radius: 18px;
  word-wrap: break-word;
  background: ${props => props.role === 'user'
    ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    : '#f0f0f0'};
  color: ${props => props.role === 'user' ? 'white' : '#333'};
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  margin-bottom: 0.5rem;
  font-size: 1.05rem;
  
  ${props => props.error && `
    background: #fee;
    color: #c33;
    border: 1px solid #fcc;
  `}
`

const MessageContent = styled.div`
  line-height: 1.6;
  white-space: pre-wrap;
`

const SourcesList = styled.div`
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid rgba(0,0,0,0.1);
  font-size: 0.85rem;
  opacity: 0.8;
`

const SourceItem = styled.div`
  margin-top: 0.25rem;
`

const Timestamp = styled.div`
  font-size: 0.75rem;
  margin-top: 0.5rem;
  opacity: 0.7;
`

function MessageList({ messages, language }) {
  const t = translations[language] || translations.fr

  const formatTime = (timestamp) => {
    const date = new Date(timestamp)
    return date.toLocaleTimeString(language === 'ar' ? 'ar-MA' : 'fr-FR', { hour: '2-digit', minute: '2-digit' })
  }

  return (
    <MessageContainer>
      {messages.map((message) => (
        <Message key={message.id} role={message.role}>
          <MessageBubble role={message.role} error={message.error}>
            <MessageContent>{message.content}</MessageContent>
            {message.metadata?.sources && message.metadata.sources.length > 0 && (
              <SourcesList>
                <strong>{language === 'ar' ? 'المصادر:' : language === 'en' ? 'Sources:' : 'Sources :'}</strong>
                {message.metadata.sources.map((source, idx) => (
                  <SourceItem key={idx}>• {source.title || source.category}</SourceItem>
                ))}
              </SourcesList>
            )}
            <Timestamp>{formatTime(message.created_at)}</Timestamp>
          </MessageBubble>
        </Message>
      ))}
    </MessageContainer>
  )
}

export default MessageList

