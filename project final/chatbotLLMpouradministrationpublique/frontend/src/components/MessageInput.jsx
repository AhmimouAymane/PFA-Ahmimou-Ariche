import React, { useState, useRef, useEffect } from 'react'
import styled from 'styled-components'
import { FiSend } from 'react-icons/fi'
import { translations } from '../translations'

const InputContainer = styled.div`
  padding: 1rem 2rem;
  background: white;
  border-top: 1px solid #e0e0e0;
`

const InputWrapper = styled.div`
  display: flex;
  gap: 0.5rem;
  align-items: flex-end;
`

const Input = styled.textarea`
  flex: 1;
  padding: 0.75rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 20px;
  font-size: 1rem;
  font-family: inherit;
  resize: none;
  max-height: 120px;
  min-height: 44px;
  line-height: 1.5;
  
  &:focus {
    outline: none;
    border-color: #667eea;
  }
  
  &:disabled {
    background: #f5f5f5;
    cursor: not-allowed;
  }
`

const SendButton = styled.button`
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: transform 0.2s, box-shadow 0.2s;
  
  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(102, 126, 234, 0.4);
  }
  
  &:active:not(:disabled) {
    transform: translateY(0);
  }
  
  &:disabled {
    background: #ccc;
    cursor: not-allowed;
  }
`

function MessageInput({ onSendMessage, disabled, language }) {
  const [message, setMessage] = useState('')
  const textareaRef = useRef(null)

  const t = translations[language] || translations.fr

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`
    }
  }, [message])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (message.trim() && !disabled) {
      onSendMessage(message.trim())
      setMessage('')
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto'
      }
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <InputContainer>
      <InputWrapper>
        <Input
          ref={textareaRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={t.placeholder}
          disabled={disabled}
          rows={1}
        />
        <SendButton
          onClick={handleSubmit}
          disabled={disabled || !message.trim()}
        >
          <FiSend />
          {t.send}
        </SendButton>
      </InputWrapper>
    </InputContainer>
  )
}

export default MessageInput

