<script setup>
import { ref, reactive } from 'vue'

const loading = ref(false)
const error   = ref('')
const showPwd = ref(false)
const form    = reactive({ username: '', password: '' })

const DEMO = {
  'patient':  { password: 'patient123', role: 'Patient', full_name: 'Diallo Mamadou',  nss: 'PAT-00001', first_name: 'Mamadou',   last_name: 'Diallo',  prenom: 'Mamadou',   nom: 'Diallo' },
  'patient2': { password: 'patient123', role: 'Patient', full_name: 'Koné Fatoumata',  nss: 'PAT-00002', first_name: 'Fatoumata', last_name: 'Koné',    prenom: 'Fatoumata', nom: 'Koné' },
}

function remplir(u, p) { form.username = u; form.password = p }

async function handleLogin() {
  error.value   = ''
  loading.value = true
  const username = form.username.toLowerCase().trim()
  const password = form.password

  const demo = DEMO[username]
  if (demo && demo.password === password) {
    localStorage.setItem('sghl_token', 'demo_token_' + Date.now())
    localStorage.setItem('sghl_user',  JSON.stringify({ username, ...demo }))
    window.location.href = '/patient/accueil'
    return
  }

  try {
    const res = await fetch('/api/v1/auth/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    })
    if (!res.ok) throw new Error()
    const data = await res.json()
    localStorage.setItem('sghl_token', data.access)
    localStorage.setItem('sghl_user',  JSON.stringify(data.user || { username, role: 'Patient', full_name: username }))
    window.location.href = '/patient/accueil'
  } catch {
    error.value   = 'Identifiants incorrects.'
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex flex-col"
    style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 50%, #e0e7ff 100%)">

    <div class="bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between shadow-sm">
      <a href="/" class="flex items-center gap-2 text-gray-700 hover:text-blue-700 transition-colors">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
        <span class="text-sm font-medium">Retour au site</span>
      </a>
      <span class="font-bold text-gray-900 text-sm">DIGNE HOSPITAL</span>
    </div>

    <div class="flex-1 flex items-center justify-center p-6">
      <div class="w-full max-w-md">
        <div class="bg-white rounded-2xl shadow-xl p-8 border border-blue-100">
          <div class="inline-flex items-center gap-2 bg-blue-100 text-blue-700 rounded-full px-4 py-1.5 text-sm font-semibold mb-5">
            👤 Espace Patient
          </div>
          <h2 class="text-2xl font-extrabold text-gray-900 mb-1">Connexion patient</h2>
          <p class="text-gray-500 text-sm mb-5">Accédez à votre dossier médical en ligne.</p>

          <form @submit.prevent="handleLogin" class="space-y-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Identifiant patient</label>
              <input v-model="form.username" type="text" class="input-field"
                placeholder="patient ou patient2" required autocomplete="username" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Mot de passe</label>
              <div class="relative">
                <input v-model="form.password" :type="showPwd ? 'text' : 'password'"
                  class="input-field pr-10" placeholder="••••••••" required autocomplete="current-password" />
                <button type="button" @click="showPwd = !showPwd"
                  class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-blue-600">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M15 12a3 3 0 11-6 0 3 3 0 016 0zM2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                  </svg>
                </button>
              </div>
            </div>

            <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3">
              {{ error }}
            </div>

            <button type="submit" :disabled="loading"
              class="w-full py-3 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm transition-all flex items-center justify-center gap-2 disabled:opacity-60">
              <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
              </svg>
              {{ loading ? 'Connexion...' : 'Accéder à mon espace' }}
            </button>
          </form>

          <!-- Démo -->
          <div class="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
            <p class="text-xs font-bold text-green-800 mb-2">🧪 Comptes démo</p>
            <div class="flex gap-2">
              <button type="button" @click="remplir('patient','patient123')"
                class="flex-1 py-2 rounded-lg bg-white border border-green-200 hover:bg-green-100 text-xs font-mono font-bold text-green-800 transition-colors">
                patient / patient123
              </button>
              <button type="button" @click="remplir('patient2','patient123')"
                class="flex-1 py-2 rounded-lg bg-white border border-green-200 hover:bg-green-100 text-xs font-mono font-bold text-green-800 transition-colors">
                patient2 / patient123
              </button>
            </div>
          </div>

          <div class="mt-4 flex gap-2">
            <a href="/login/professionnel" class="flex-1 text-center py-2 rounded-lg bg-blue-50 text-blue-700 text-xs font-semibold hover:bg-blue-100 transition-colors">
              🩺 Espace Pro
            </a>
            <a href="/login/admin" class="flex-1 text-center py-2 rounded-lg bg-slate-50 text-slate-700 text-xs font-semibold hover:bg-slate-100 transition-colors">
              ⚙️ Administration
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
