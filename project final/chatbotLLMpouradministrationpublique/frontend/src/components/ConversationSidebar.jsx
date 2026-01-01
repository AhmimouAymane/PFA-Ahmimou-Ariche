import React, { useState, useEffect } from 'react'
import styled from 'styled-components'
import { chatService } from '../services/chatService'
import { FiMessageSquare, FiPlus, FiTrash2 } from 'react-icons/fi'
import { translations } from '../translations'

const Sidebar = styled.div.attrs(props => ({
  className: props.$isRTL ? 'rtl' : 'ltr'
}))`
  width: 300px;
  background: #2d3748;
  color: white;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #4a5568;
`

const SidebarHeader = styled.div`
  padding: 1.5rem;
  border-bottom: 1px solid #4a5568;
`

const SidebarTitle = styled.h2`
  margin: 0;
  font-size: 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`

const NewChatButton = styled.button`
  width: 100%;
  margin-top: 1rem;
  padding: 0.75rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: background 0.3s;
  
  &:hover {
    background: #5568d3;
  }
`

const ConversationsList = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
`

const ConversationItem = styled.div`
  padding: 1rem;
  margin-bottom: 0.5rem;
  background: ${props => props.active ? '#4a5568' : 'transparent'};
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  &:hover {
    background: #4a5568;
  }
`

const ConversationTitle = styled.div`
  font-weight: ${props => props.active ? 'bold' : 'normal'};
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
`

const DeleteButton = styled.button`
  padding: 0.25rem;
  background: transparent;
  color: #cbd5e0;
  border: none;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s;
  
  ${ConversationItem}:hover & {
    opacity: 1;
  }
  
  &:hover {
    color: #fc8181;
  }
`

const EmptyState = styled.div`
  text-align: center;
  padding: 2rem;
  color: #cbd5e0;
`

function ConversationSidebar({ currentConversationId, onSelectConversation, onNewConversation, language }) {
  const [conversations, setConversations] = useState([])
  const [loading, setLoading] = useState(true)

  const t = translations[language] || translations.fr
  const isRTL = language === 'ar' || language === 'am'

  useEffect(() => {
    loadConversations()
  }, [currentConversationId])

  const loadConversations = async () => {
    try {
      setLoading(true)
      const convs = await chatService.getConversations()
      setConversations(convs || [])
    } catch (error) {
      console.error('Error loading conversations:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleNewChat = () => {
    onNewConversation(null)
  }

  const handleSelect = (convId) => {
    onSelectConversation(convId)
  }

  const handleDelete = async (e, convId) => {
    e.stopPropagation()
    // In a real app, you'd have a delete endpoint
    // For now, just reload conversations
    loadConversations()
  }

  return (
    <Sidebar $isRTL={isRTL}>
      <SidebarHeader>
        <SidebarTitle>
          <FiMessageSquare />
          {t.conversations}
        </SidebarTitle>
        <NewChatButton onClick={handleNewChat}>
          <FiPlus />
          {t.new_conversation}
        </NewChatButton>
      </SidebarHeader>
      <ConversationsList>
        {loading ? (
          <EmptyState>{t.loading}</EmptyState>
        ) : conversations.length === 0 ? (
          <EmptyState>
            {t.no_conversations}
            <br />
            <small>{t.create_new_to_start}</small>
          </EmptyState>
        ) : (
          conversations.map(conv => (
            <ConversationItem
              key={conv.id}
              active={conv.id === currentConversationId}
              onClick={() => handleSelect(conv.id)}
            >
              <ConversationTitle active={conv.id === currentConversationId}>
                {conv.title || `${t.new_conversation.replace('Nouvelle ', '')} ${conv.id}`}
              </ConversationTitle>
              <DeleteButton onClick={(e) => handleDelete(e, conv.id)}>
                <FiTrash2 />
              </DeleteButton>
            </ConversationItem>
          ))
        )}
      </ConversationsList>
    </Sidebar>
  )
}

export default ConversationSidebar

