import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const chatService = {
  async sendMessage(message, conversationId = null, language = null) {
    const response = await api.post('/api/chat/message', {
      message,
      conversation_id: conversationId,
      language
    })
    return response.data
  },

  async getConversations() {
    const response = await api.get('/api/chat/conversations')
    return response.data.conversations
  },

  async getConversation(conversationId) {
    const response = await api.get(`/api/chat/conversation/${conversationId}`)
    return response.data
  }
}

