import React from 'react'
import styled from 'styled-components'

const Select = styled.select`
  padding: 0.5rem 1rem;
  background: rgba(255,255,255,0.2);
  color: white;
  border: 1px solid rgba(255,255,255,0.3);
  border-radius: 5px;
  font-size: 0.9rem;
  cursor: pointer;
  font-family: 'Noto Sans Arabic', 'Noto Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  
  &:focus {
    outline: none;
    background: rgba(255,255,255,0.3);
  }
  
  option {
    background: #667eea;
    color: white;
    font-family: 'Noto Sans Arabic', 'Noto Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    padding: 0.5rem;
  }
`

function LanguageSelector({ currentLanguage, onLanguageChange }) {
  const languages = [
    { code: 'fr', label: 'Français' },
    { code: 'ar', label: 'العربية' },
    { code: 'am', label: 'ⵜⴰⵎⴰⵣⵉⵖⵜ' },
    { code: 'en', label: 'English' }
  ]

  return (
    <Select
      value={currentLanguage}
      onChange={(e) => onLanguageChange(e.target.value)}
    >
      {languages.map(lang => (
        <option key={lang.code} value={lang.code}>
          {lang.label}
        </option>
      ))}
    </Select>
  )
}

export default LanguageSelector

