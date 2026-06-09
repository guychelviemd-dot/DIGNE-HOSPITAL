<script setup>
import { ref, computed } from 'vue'

const showModal = ref(false)
const activeTab = ref('a-venir')

const sessions = ref([
  { id: 1, patient: 'Diallo Mamadou', medecin: 'Dr. Camara', date: '2025-06-13', heure: '10:00', motif: 'Suivi diabète type 2', statut: 'Planifiée', duree: 20 },
  { id: 2, patient: 'Koné Fatoumata', medecin: 'Dr. Bah', date: '2025-06-13', heure: '11:30', motif: 'Contrôle post-opératoire', statut: 'En attente', duree: 15 },
  { id: 3, patient: 'Traoré Ibrahim', medecin: 'Dr. Diallo', date: '2025-06-12', heure: '14:00', motif: 'Renouvellement ordonnance', statut: 'Terminée', duree: 12 },
  { id: 4, patient: 'Bah Aissatou', medecin: 'Dr. Camara', date: '2025-06-12', heure: '09:00', motif: 'Consultation grossesse', statut: 'Terminée', duree: 25 },
])

const statutColor = {
  'Planifiée': 'badge-info', 'En attente': 'badge-warning',
  'En cours': 'badge-chu', 'Terminée': 'badge-success', 'Annulée': 'badge-danger',
}

const filtered = computed(() =>
  sessions.value.filter(s =>
    activeTab.value === 'tous' ||
    (activeTab.value === 'a-venir' && ['Planifiée', 'En attente'].includes(s.statut)) ||
    (activeTab.value === 'terminees' && s.statut === 'Terminée')
  )
)

const stats = computed(() => ({
  planifiees: sessions.value.filter(s => s.statut === 'Planifiée').length,
  en_attente: sessions.value.filter(s => s.statut === 'En attente').length,
  terminees: sessions.value.filter(s => s.statut === 'Terminée').length,
  duree_moy: Math.round(sessions.value.reduce((s, x) => s + x.duree, 0) / sessions.value.length),
}))
</script>

<template>
  <div class="space-y-5">

    <div class="flex items-center justify-between">
      <div>
        <h2 class="page-title">📹 Téléconsultation</h2>
        <p class="text-sm text-gray-500 mt-0.5">Consultations vidéo sécurisées médecin-patient</p>
      </div>
      <button @click="showModal = true" class="btn-primary">+ Planifier session</button>
    </div>

    <!-- KPIs -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
      <div class="stat-card p-4 flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center text-lg">📅</div>
        <div><p class="text-xl font-extrabold text-blue-600">{{ stats.planifiees }}</p><p class="text-xs text-gray-500">Planifiées</p></div>
      </div>
      <div class="stat-card p-4 flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg bg-amber-100 flex items-center justify-center text-lg">⏳</div>
        <div><p class="text-xl font-extrabold text-amber-600">{{ stats.en_attente }}</p><p class="text-xs text-gray-500">En attente</p></div>
      </div>
      <div class="stat-card p-4 flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center text-lg">✅</div>
        <div><p class="text-xl font-extrabold text-green-600">{{ stats.terminees }}</p><p class="text-xs text-gray-500">Terminées</p></div>
      </div>
      <div class="stat-card p-4 flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg bg-violet-100 flex items-center justify-center text-lg">⏱️</div>
        <div><p class="text-xl font-extrabold text-violet-600">{{ stats.duree_moy }}<span class="text-sm font-normal">min</span></p><p class="text-xs text-gray-500">Durée moyenne</p></div>
      </div>
    </div>

    <!-- Info sécurité -->
    <div class="alert-info-banner flex items-center gap-3">
      <span class="text-blue-600 text-lg">🔒</span>
      <p class="text-sm text-blue-800">
        <strong>Connexions chiffrées end-to-end</strong> — Conformité RGPD & HDS (Hébergeur de Données de Santé).
        Liens de connexion à usage unique, expiration automatique après la session.
      </p>
    </div>

    <!-- Tabs -->
    <div class="flex gap-1 bg-gray-100 rounded-lg p-1 w-fit">
      <button v-for="tab in [{k:'a-venir',l:'À venir'},{k:'terminees',l:'Terminées'},{k:'tous',l:'Toutes'}]" :key="tab.k"
        @click="activeTab = tab.k"
        :class="['px-3 py-1.5 rounded-md text-xs font-semibold transition-all', activeTab === tab.k ? 'bg-white text-blue-700 shadow-sm' : 'text-gray-500']">
        {{ tab.l }}
      </button>
    </div>

    <!-- Table -->
    <div class="stat-card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="table-header">
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Patient</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Médecin</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Date / Heure</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Motif</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Durée</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Statut</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in filtered" :key="s.id" class="table-row border-b border-gray-50">
              <td class="px-4 py-3 font-semibold text-gray-900">{{ s.patient }}</td>
              <td class="px-4 py-3 text-gray-600">{{ s.medecin }}</td>
              <td class="px-4 py-3">
                <p class="text-gray-700">{{ s.date }}</p>
                <p class="text-xs font-mono text-gray-400">{{ s.heure }}</p>
              </td>
              <td class="px-4 py-3 text-xs text-gray-600">{{ s.motif }}</td>
              <td class="px-4 py-3 text-xs text-gray-600">{{ s.duree }} min</td>
              <td class="px-4 py-3">
                <span :class="['text-xs font-medium px-2.5 py-1 rounded-full', statutColor[s.statut]]">{{ s.statut }}</span>
              </td>
              <td class="px-4 py-3">
                <div class="flex gap-2">
                  <button v-if="['Planifiée','En attente'].includes(s.statut)"
                    class="btn-primary text-xs py-1 px-3">📹 Rejoindre</button>
                  <button v-else class="text-blue-600 text-xs font-medium">Voir →</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal -->
    <Teleport to="body">
      <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
        <div class="modal-box">
          <h3 class="text-lg font-bold text-gray-900 mb-5">Planifier une téléconsultation</h3>
          <form @submit.prevent="showModal = false" class="space-y-4">
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">Patient</label>
                <select class="input-field"><option>Diallo Mamadou</option></select>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">Médecin</label>
                <select class="input-field"><option>Dr. Camara</option></select>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">Date</label>
                <input type="date" class="input-field" required />
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">Heure</label>
                <input type="time" class="input-field" required />
              </div>
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1">Motif</label>
              <input class="input-field" placeholder="Motif de la téléconsultation" required />
            </div>
            <div class="flex gap-3 pt-2">
              <button type="button" @click="showModal = false" class="btn-secondary flex-1">Annuler</button>
              <button type="submit" class="btn-primary flex-1">Planifier & Envoyer lien</button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>

  </div>
</template>
