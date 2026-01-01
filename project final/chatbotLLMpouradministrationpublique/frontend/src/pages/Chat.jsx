import React, { useState } from 'react'
import styled from 'styled-components'
import ChatInterface from '../components/ChatInterface'
import ConversationSidebar from '../components/ConversationSidebar'

const ChatPage = styled.div`
  display: flex;
  height: 100vh;
  overflow: hidden;
`

function Chat() {
  const [currentConversationId, setCurrentConversationId] = useState(null)
  const [language, setLanguage] = useState('fr')

  const handleSelectConversation = (conversationId) => {
    setCurrentConversationId(conversationId)
  }

  const handleNewConversation = () => {
    setCurrentConversationId(null)
  }

  const handleConversationChange = (conversationId) => {
    setCurrentConversationId(conversationId)
  }

  const handleLanguageChange = (newLang) => {
    setLanguage(newLang)
  }

  return (
    <ChatPage>
      <ConversationSidebar
        currentConversationId={currentConversationId}
        onSelectConversation={handleSelectConversation}
        onNewConversation={handleNewConversation}
        language={language}
      />
      <ChatInterface
        conversationId={currentConversationId}
        onConversationChange={handleConversationChange}
        language={language}
        onLanguageUpdate={handleLanguageChange}
      />
    </ChatPage>
  )
}

export default Chat

