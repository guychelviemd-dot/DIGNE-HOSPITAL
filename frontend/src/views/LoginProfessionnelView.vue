<script setup>
import { ref } from 'vue'

// ── Comptes de démonstration ──────────────────────────────────────
const COMPTES = {
  medecin:    { mdp: 'medecin123',    role: 'Médecin',    nom: 'Dr. Camara Alpha',  service: 'Médecine interne' },
  infirmier:  { mdp: 'infirmier123',  role: 'Infirmier',  nom: 'Kouyaté Ibrahima',  service: 'Urgences' },
  biologiste: { mdp: 'biologiste123', role: 'Biologiste', nom: 'Dr. Diallo Oumar',  service: 'Laboratoire' },
  pharmacien: { mdp: 'pharmacien123', role: 'Pharmacien', nom: 'Sylla Kadiatou',    service: 'Pharmacie' },
  radiologue: { mdp: 'radiologue123', role: 'Médecin',    nom: 'Dr. Kouyaté Sekou', service: 'Imagerie' },
  chirurgien: { mdp: 'chirurgien123', role: 'Médecin',    nom: 'Dr. Barry Mamadou', service: 'Chirurgie' },
  caissier:   { mdp: 'caissier123',   role: 'Caissier',   nom: 'Traoré Aminata',    service: 'Facturation' },
  admin:      { mdp: 'admin123',      role: 'Admin',      nom: 'Traoré Moussa',     service: 'Direction' },
  test:       { mdp: 'test',          role: 'Admin',      nom: 'Utilisateur Test',  service: 'Test' },
}

const identifiant = ref('')
const motdepasse  = ref('')
const erreur      = ref('')
const chargement  = ref(false)
const voirMdp     = ref(false)

// Remplir les champs depuis un bouton démo
function remplir(id, mdp) {
  identifiant.value = id
  motdepasse.value  = mdp
  erreur.value      = ''
}

// Connexion
function connecter() {
  erreur.value     = ''
  chargement.value = true

  const id  = identifiant.value.trim().toLowerCase()
  const mdp = motdepasse.value

  if (!id || !mdp) {
    erreur.value     = 'Veuillez remplir tous les champs.'
    chargement.value = false
    return
  }

  const compte = COMPTES[id]

  if (compte && compte.mdp === mdp) {
    // Sauvegarder dans localStorage
    const token = 'demo_' + id + '_' + Date.now()
    const user  = {
      username:   id,
      role:       compte.role,
      full_name:  compte.nom,
      service:    compte.service,
      first_name: compte.nom.split(' ')[0],
      last_name:  compte.nom.split(' ').slice(1).join(' '),
    }
    localStorage.setItem('sghl_token', token)
    localStorage.setItem('sghl_user',  JSON.stringify(user))
    // Redirection forcée
    router.push('/dashboard/accueil')
    return
  }

  erreur.value     = 'Identifiant ou mot de passe incorrect.'
  chargement.value = false
}

const listeDemos = [
  ['medecin',    'medecin123'],
  ['infirmier',  'infirmier123'],
  ['biologiste', 'biologiste123'],
  ['pharmacien', 'pharmacien123'],
  ['radiologue', 'radiologue123'],
  ['chirurgien', 'chirurgien123'],
  ['admin',      'admin123'],
  ['caissier',   'caissier123'],
  ['test',       'test'],
]
</script>

<template>
  <div class="min-h-screen flex flex-col" style="background:#f4f7fb">

    <!-- Barre du haut -->
    <div class="bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between shadow-sm">
      <a href="/" class="flex items-center gap-2 text-gray-600 hover:text-blue-700 text-sm font-medium">
        ← Retour au site
      </a>
      <span class="font-bold text-gray-900 text-sm">🏥 DIGNE HOSPITAL</span>
    </div>

    <div class="flex-1 flex items-center justify-center p-6">
      <div class="w-full max-w-md">
        <div class="bg-white rounded-2xl shadow-lg p-8 border border-blue-100">

          <h2 class="text-2xl font-extrabold text-gray-900 mb-1">🩺 Espace Professionnel</h2>
          <p class="text-gray-500 text-sm mb-6">Connectez-vous avec votre identifiant.</p>

          <!-- Formulaire -->
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Identifiant</label>
              <input
                v-model="identifiant"
                type="text"
                class="input-field"
                placeholder="medecin, admin, biologiste..."
                autocomplete="username"
                @keyup.enter="connecter"
              />
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Mot de passe</label>
              <div class="relative">
                <input
                  v-model="motdepasse"
                  :type="voirMdp ? 'text' : 'password'"
                  class="input-field pr-10"
                  placeholder="••••••••"
                  autocomplete="current-password"
                  @keyup.enter="connecter"
                />
                <button type="button" @click="voirMdp = !voirMdp"
                  class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-blue-600 text-xs">
                  {{ voirMdp ? '🙈' : '👁️' }}
                </button>
              </div>
            </div>

            <!-- Erreur -->
            <div v-if="erreur" class="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3">
              ❌ {{ erreur }}
            </div>

            <!-- Bouton connexion -->
            <button
              @click="connecter"
              :disabled="chargement"
              class="w-full py-3 rounded-lg bg-blue-700 hover:bg-blue-800 text-white font-bold text-sm transition-all disabled:opacity-60"
            >
              {{ chargement ? '⏳ Connexion...' : '🔐 Accéder au système clinique' }}
            </button>
          </div>

          <!-- Comptes démo -->
          <div class="mt-6 p-4 bg-green-50 border border-green-200 rounded-xl">
            <p class="text-xs font-bold text-green-800 mb-3">
              🧪 Comptes démo — cliquez pour remplir, puis appuyez sur le bouton bleu
            </p>
            <div class="grid grid-cols-3 gap-2">
              <button
                v-for="[id, mdp] in listeDemos"
                :key="id"
                type="button"
                @click="remplir(id, mdp)"
                class="py-2 px-1 rounded-lg bg-white border-2 hover:border-blue-400 hover:bg-blue-50 transition-all text-center"
                :class="identifiant === id ? 'border-blue-500 bg-blue-50' : 'border-green-200'"
              >
                <span class="text-xs font-bold text-gray-800 block">{{ id }}</span>
                <span class="text-[10px] text-gray-500">{{ mdp }}</span>
              </button>
            </div>
          </div>

          <!-- Autres portails -->
          <div class="mt-4 flex gap-2">
            <a href="/login/patient"
              class="flex-1 text-center py-2 rounded-lg bg-blue-50 text-blue-700 text-xs font-semibold hover:bg-blue-100 transition-colors">
              👤 Espace Patient
            </a>
            <a href="/login/admin"
              class="flex-1 text-center py-2 rounded-lg bg-slate-50 text-slate-700 text-xs font-semibold hover:bg-slate-100 transition-colors">
              ⚙️ Administration
            </a>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>
