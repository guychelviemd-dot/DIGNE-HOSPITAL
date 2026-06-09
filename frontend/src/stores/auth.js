import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const DEMO_USERS = {
  'medecin':    { password: 'medecin123',    role: 'Médecin',    full_name: 'Dr. Camara Alpha',  service: 'Médecine interne', first_name: 'Alpha',     last_name: 'Camara' },
  'infirmier':  { password: 'infirmier123',  role: 'Infirmier',  full_name: 'Kouyaté Ibrahima',  service: 'Urgences',         first_name: 'Ibrahima',  last_name: 'Kouyaté' },
  'biologiste': { password: 'biologiste123', role: 'Biologiste', full_name: 'Dr. Diallo Oumar',  service: 'Laboratoire',      first_name: 'Oumar',     last_name: 'Diallo' },
  'pharmacien': { password: 'pharmacien123', role: 'Pharmacien', full_name: 'Sylla Kadiatou',    service: 'Pharmacie',        first_name: 'Kadiatou',  last_name: 'Sylla' },
  'radiologue': { password: 'radiologue123', role: 'Médecin',    full_name: 'Dr. Kouyaté Sekou', service: 'Imagerie',         first_name: 'Sekou',     last_name: 'Kouyaté' },
  'chirurgien': { password: 'chirurgien123', role: 'Médecin',    full_name: 'Dr. Barry Mamadou', service: 'Chirurgie',        first_name: 'Mamadou',   last_name: 'Barry' },
  'caissier':   { password: 'caissier123',   role: 'Caissier',   full_name: 'Traoré Aminata',    service: 'Facturation',      first_name: 'Aminata',   last_name: 'Traoré' },
  'admin':      { password: 'admin123',      role: 'Admin',      full_name: 'Traoré Moussa',     service: 'Direction',        first_name: 'Moussa',    last_name: 'Traoré' },
  'test':       { password: 'test',          role: 'Admin',      full_name: 'Utilisateur Test',  service: 'Test',             first_name: 'Test',      last_name: 'User' },
  'patient':    { password: 'patient123',    role: 'Patient',    full_name: 'Diallo Mamadou',    nss: 'PAT-00001',            first_name: 'Mamadou',   last_name: 'Diallo',    prenom: 'Mamadou',   nom: 'Diallo' },
  'patient2':   { password: 'patient123',    role: 'Patient',    full_name: 'Koné Fatoumata',    nss: 'PAT-00002',            first_name: 'Fatoumata', last_name: 'Koné',      prenom: 'Fatoumata', nom: 'Koné' },
  'dr.camara':  { password: '1234',          role: 'Médecin',    full_name: 'Dr. Camara Alpha',  service: 'Médecine interne', first_name: 'Alpha',     last_name: 'Camara' },
}

export const useAuthStore = defineStore('auth', () => {
  // Initialisation depuis localStorage
  const token = ref(localStorage.getItem('sghl_token') || null)
  const user  = ref((() => {
    try { return JSON.parse(localStorage.getItem('sghl_user')) } catch { return null }
  })())

  const isAuthenticated = computed(() => !!token.value)

  async function login(credentials) {
    const username = (credentials.username || '').toLowerCase().trim()
    const password = credentials.password || ''

    // Mode démo
    const demo = DEMO_USERS[username]
    if (demo && demo.password === password) {
      const userData = { username, ...demo }
      token.value = 'demo_token_' + Date.now()
      user.value  = userData
      localStorage.setItem('sghl_token', token.value)
      localStorage.setItem('sghl_user',  JSON.stringify(userData))
      return userData
    }

    // API réelle
    try {
      const { default: api } = await import('@/services/api')
      const { data } = await api.post('/auth/login/', { username, password })
      token.value = data.access
      user.value  = data.user || { username, role: 'Médecin', full_name: username }
      localStorage.setItem('sghl_token', token.value)
      localStorage.setItem('sghl_user',  JSON.stringify(user.value))
      return user.value
    } catch {
      throw new Error('Identifiants incorrects')
    }
  }

  function logout() {
    token.value = null
    user.value  = null
    localStorage.removeItem('sghl_token')
    localStorage.removeItem('sghl_user')
  }

  return { token, user, isAuthenticated, login, logout }
})
