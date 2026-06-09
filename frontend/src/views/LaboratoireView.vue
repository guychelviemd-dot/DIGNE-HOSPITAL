<script setup>
import { ref, computed } from 'vue'

const search = ref('')
const activeFilter = ref('Tous')

const examens = ref([
  { id: 1, patient: 'Diallo Mamadou', type: 'NFS', prescripteur: 'Dr. Camara', date: '2025-06-12', priorite: 'Urgent', statut: 'Prélèvement', technicien: 'Lab. Kouyaté' },
  { id: 2, patient: 'Koné Fatoumata', type: 'Glycémie', prescripteur: 'Dr. Bah', date: '2025-06-12', priorite: 'Normal', statut: 'Saisie résultats', technicien: 'Lab. Kouyaté' },
  { id: 3, patient: 'Traoré Ibrahim', type: 'ECG', prescripteur: 'Dr. Diallo', date: '2025-06-11', priorite: 'Normal', statut: 'Validé', technicien: 'Lab. Sylla' },
  { id: 4, patient: 'Camara Sekou', type: 'Radiographie', prescripteur: 'Dr. Camara', date: '2025-06-11', priorite: 'Urgent', statut: 'Publié', technicien: 'Lab. Sylla' },
  { id: 5, patient: 'Bah Aissatou', type: 'Urine ECBU', prescripteur: 'Dr. Bah', date: '2025-06-10', priorite: 'Normal', statut: 'Commande', technicien: '-' },
])

const workflow = ['Commande', 'Prélèvement', 'Affectation', 'Saisie résultats', 'Validé', 'Publié']

const filters = ['Tous', ...workflow]

const filtered = computed(() =>
  examens.value.filter(e =>
    (activeFilter.value === 'Tous' || e.statut === activeFilter.value) &&
    e.patient.toLowerCase().includes(search.value.toLowerCase())
  )
)

const statutColor = {
  'Commande': 'badge-info',
  'Prélèvement': 'badge-warning',
  'Affectation': 'badge-warning',
  'Saisie résultats': 'badge-violet',
  'Validé': 'badge-success',
  'Publié': 'badge-success',
}

function workflowStep(statut) {
  return workflow.indexOf(statut)
}
</script>

<template>
  <div class="space-y-5">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="page-title">Laboratoire (LIS)</h2>
        <p class="text-sm text-violet-500 mt-0.5">Gestion des examens biologiques</p>
      </div>
      <button class="btn-primary">+ Prescrire examen</button>
    </div>

    <!-- Score module 100% -->
    <div class="stat-card p-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center text-white text-xl shadow-lg">🔬</div>
          <div>
            <p class="text-sm font-bold text-gray-900">Module Laboratoire</p>
            <p class="text-xs text-violet-600">Conformité aux spécifications</p>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <div class="text-right">
            <p class="text-2xl font-extrabold bg-gradient-to-r from-violet-600 to-purple-600 bg-clip-text text-transparent">100%</p>
            <p class="text-xs text-green-600 font-semibold">✓ Opérationnel</p>
          </div>
          <div class="w-12 h-12 relative">
            <svg class="w-12 h-12 -rotate-90" viewBox="0 0 36 36">
              <circle cx="18" cy="18" r="14" fill="none" stroke="#e9d5ff" stroke-width="3.5"/>
              <circle cx="18" cy="18" r="14" fill="none" stroke="url(#score-gradient)" stroke-width="3.5" stroke-dasharray="88 88" stroke-linecap="round"/>
            </svg>
            <defs>
              <linearGradient id="score-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:#a855f7"/>
                <stop offset="100%" style="stop-color:#7e22ce"/>
              </linearGradient>
            </defs>
          </div>
        </div>
      </div>
    </div>

    <!-- Workflow pipeline -->
    <div class="stat-card p-5">
      <p class="section-title mb-4">Pipeline des examens</p>
      <div class="flex items-center gap-0 overflow-x-auto">
        <div v-for="(step, i) in workflow" :key="step" class="flex items-center">
          <div class="flex flex-col items-center min-w-[100px]">
            <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold', i <= 3 ? 'bg-gradient-to-br from-violet-600 to-purple-600 text-white shadow-lg' : 'bg-violet-100 text-violet-600']">
              {{ i + 1 }}
            </div>
            <p class="text-xs text-center mt-1.5 font-medium text-gray-600 leading-tight">{{ step }}</p>
            <p class="text-xs text-violet-600 font-bold">{{ examens.filter(e => e.statut === step).length }}</p>
          </div>
          <div v-if="i < workflow.length - 1" class="w-8 h-0.5 bg-violet-200 mb-5"></div>
        </div>
      </div>
    </div>

    <!-- Filters + search -->
    <div class="stat-card p-4 flex flex-wrap gap-3 items-center">
      <input v-model="search" class="input-field max-w-xs" placeholder="🔍  Rechercher..." />
      <div class="flex gap-2 flex-wrap">
        <button
          v-for="f in filters" :key="f"
          @click="activeFilter = f"
          :class="['px-3 py-1.5 rounded-lg text-xs font-medium transition-all', activeFilter === f ? 'bg-gradient-to-r from-violet-600 to-purple-600 text-white shadow-md' : 'bg-violet-50 text-violet-700 hover:bg-violet-100']"
        >
          {{ f }}
        </button>
      </div>
    </div>

    <!-- Table -->
    <div class="stat-card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="table-header">
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Patient</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Type d'examen</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Prescripteur</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Date</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Priorité</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Statut</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="e in filtered" :key="e.id" class="table-row border-b border-gray-50">
              <td class="px-4 py-3 font-medium text-gray-900">{{ e.patient }}</td>
              <td class="px-4 py-3 text-gray-600">{{ e.type }}</td>
              <td class="px-4 py-3 text-gray-500">{{ e.prescripteur }}</td>
              <td class="px-4 py-3 text-gray-500">{{ e.date }}</td>
              <td class="px-4 py-3">
                <span :class="['text-xs font-medium px-2.5 py-1 rounded-full', e.priorite === 'Urgent' ? 'badge-danger' : 'badge-info']">
                  {{ e.priorite }}
                </span>
              </td>
              <td class="px-4 py-3">
                <span :class="['text-xs font-medium px-2.5 py-1 rounded-full', statutColor[e.statut]]">{{ e.statut }}</span>
              </td>
              <td class="px-4 py-3">
                <button class="text-violet-600 hover:text-violet-800 text-xs font-medium">Traiter →</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
