<script setup>
import { ref, reactive } from 'vue'

const loading = ref(false)
const error   = ref('')
const showPwd = ref(false)
const form    = reactive({ username: '', password: '' })

const DEMO = {
  'admin': { password: 'admin123', role: 'Admin', full_name: 'Traoré Moussa',    service: 'Direction', first_name: 'Moussa', last_name: 'Traoré' },
  'test':  { password: 'test',     role: 'Admin', full_name: 'Utilisateur Test', service: 'Test',      first_name: 'Test',   last_name: 'User' },
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
    window.location.href = '/dashboard/accueil'
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
    localStorage.setItem('sghl_user',  JSON.stringify(data.user || { username, role: 'Admin', full_name: username }))
    window.location.href = '/dashboard/accueil'
  } catch {
    error.value   = 'Identifiants incorrects.'
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex flex-col items-center justify-center p-6"
    style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #1e1b4b 100%)">

    <div class="w-full max-w-md">
      <div class="text-center mb-6">
        <div class="w-16 h-16 rounded-2xl bg-white/10 flex items-center justify-center mx-auto mb-3">
          <svg class="w-9 h-9 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
          </svg>
        </div>
        <h1 class="text-2xl font-extrabold text-white">DIGNE HOSPITAL</h1>
        <p class="text-slate-400 text-sm mt-1">Espace Administrateur</p>
      </div>

      <div class="bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl p-8">
        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-1.5">Identifiant</label>
            <input v-model="form.username" type="text"
              class="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-2.5 text-white text-sm placeholder-gray-500 outline-none focus:border-slate-400 transition-all"
              placeholder="admin" required autocomplete="username" />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-1.5">Mot de passe</label>
            <div class="relative">
              <input v-model="form.password" :type="showPwd ? 'text' : 'password'"
                class="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-2.5 text-white text-sm placeholder-gray-500 outline-none focus:border-slate-400 transition-all pr-10"
                placeholder="••••••••" required autocomplete="current-password" />
              <button type="button" @click="showPwd = !showPwd"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0zM2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                </svg>
              </button>
            </div>
          </div>

          <div v-if="error" class="bg-red-900/30 border border-red-500/30 text-red-300 text-sm rounded-xl px-4 py-3">
            {{ error }}
          </div>

          <button type="submit" :disabled="loading"
            class="w-full py-3 rounded-xl bg-slate-600 hover:bg-slate-500 text-white font-bold text-sm transition-all flex items-center justify-center gap-2 disabled:opacity-60">
            <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
            </svg>
            {{ loading ? 'Connexion...' : 'Accéder au panneau admin' }}
          </button>
        </form>

        <!-- Démo -->
        <div class="mt-4 p-3 bg-green-900/20 border border-green-500/30 rounded-xl">
          <p class="text-xs font-bold text-green-400 mb-2">🧪 Comptes démo</p>
          <div class="flex gap-2">
            <button type="button" @click="remplir('admin','admin123')"
              class="flex-1 py-2 rounded-lg bg-white/10 hover:bg-white/20 text-xs font-mono font-bold text-green-300 transition-colors">
              admin / admin123
            </button>
            <button type="button" @click="remplir('test','test')"
              class="flex-1 py-2 rounded-lg bg-white/10 hover:bg-white/20 text-xs font-mono font-bold text-green-300 transition-colors">
              test / test
            </button>
          </div>
        </div>

        <div class="mt-4 flex gap-2">
          <a href="/login/patient" class="flex-1 text-center py-2 rounded-xl bg-white/8 text-gray-400 text-xs font-medium hover:bg-white/15 transition-colors">
            👤 Espace Patient
          </a>
          <a href="/login/professionnel" class="flex-1 text-center py-2 rounded-xl bg-white/8 text-gray-400 text-xs font-medium hover:bg-white/15 transition-colors">
            🩺 Espace Pro
          </a>
        </div>
      </div>

      <p class="text-center text-xs text-gray-600 mt-4">
        <a href="/" class="hover:text-gray-400 transition-colors">← Retour au site</a>
      </p>
    </div>
  </div>
</template>
