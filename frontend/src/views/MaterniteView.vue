<script setup>
import { ref, computed } from 'vue'

const activeTab = ref('grossesses')
const showModal = ref(false)

const grossesses = ref([
  { id: 1, patiente: 'Bah Aissatou', age: 28, sa: 32, terme: '2025-08-15', type: 'Simple', statut: 'En cours', medecin: 'Dr. Camara', consultations: 6, risque: 'Faible', groupe: 'A+' },
  { id: 2, patiente: 'Kouyaté Mariama', age: 34, sa: 38, terme: '2025-07-01', type: 'Simple', statut: 'En cours', medecin: 'Dr. Bah', consultations: 8, risque: 'Modéré', groupe: 'O+' },
  { id: 3, patiente: 'Diallo Kadiatou', age: 26, sa: 28, terme: '2025-09-10', type: 'Gémellaire', statut: 'En cours', medecin: 'Dr. Camara', consultations: 5, risque: 'Élevé', groupe: 'B+' },
  { id: 4, patiente: 'Traoré Oumou', age: 31, sa: 40, terme: '2025-06-10', type: 'Simple', statut: 'En cours', medecin: 'Dr. Bah', consultations: 9, risque: 'Faible', groupe: 'AB+' },
])

const accouchements = ref([
  { id: 1, patiente: 'Sylla Fatoumata', date: '2025-06-12', heure: '03:42', type: 'Voie basse', sage_femme: 'SF Kouyaté', poids: 3250, apgar1: 9, apgar5: 10, sexe: 'F', statut: 'Bien' },
  { id: 2, patiente: 'Camara Aminata', date: '2025-06-11', heure: '14:15', type: 'Césarienne urgente', sage_femme: 'SF Diallo', poids: 2900, apgar1: 7, apgar5: 9, sexe: 'M', statut: 'Bien' },
  { id: 3, patiente: 'Barry Hawa', date: '2025-06-10', heure: '22:30', type: 'Forceps', sage_femme: 'SF Kouyaté', poids: 3800, apgar1: 8, apgar5: 10, sexe: 'M', statut: 'Bien' },
])

const risqueColor = { 'Faible': 'badge-success', 'Modéré': 'badge-warning', 'Élevé': 'badge-danger' }
const typeColor = { 'Simple': 'badge-info', 'Gémellaire': 'badge-violet', 'Triple': 'badge-orange' }

const stats = computed(() => ({
  en_cours: grossesses.value.filter(g => g.statut === 'En cours').length,
  terme_proche: grossesses.value.filter(g => g.sa >= 37).length,
  risque_eleve: grossesses.value.filter(g => g.risque === 'Élevé').length,
  accouchements_mois: accouchements.value.length,
}))
</script>

<template>
  <div class="space-y-5">

    <div class="flex items-center justify-between">
      <div>
        <h2 class="page-title">🤱 Maternité & Obstétrique</h2>
        <p class="text-sm text-gray-500 mt-0.5">Suivi des grossesses, accouchements et nouveau-nés</p>
      </div>
      <button @click="showModal = true" class="btn-primary">+ Nouvelle grossesse</button>
    </div>

    <!-- KPIs -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
      <div class="stat-card p-4 flex items-center gap-3 border-l-4 border-pink-500">
        <div class="w-10 h-10 rounded-lg bg-pink-100 flex items-center justify-center text-lg">🤰</div>
        <div><p class="text-xl font-extrabold text-pink-600">{{ stats.en_cours }}</p><p class="text-xs text-gray-500">Grossesses en cours</p></div>
      </div>
      <div class="stat-card p-4 flex items-center gap-3 border-l-4 border-amber-400">
        <div class="w-10 h-10 rounded-lg bg-amber-100 flex items-center justify-center text-lg">⏰</div>
        <div><p class="text-xl font-extrabold text-amber-600">{{ stats.terme_proche }}</p><p class="text-xs text-gray-500">Terme ≥ 37 SA</p></div>
      </div>
      <div class="stat-card p-4 flex items-center gap-3 border-l-4 border-red-500">
        <div class="w-10 h-10 rounded-lg bg-red-100 flex items-center justify-center text-lg">⚠️</div>
        <div><p class="text-xl font-extrabold text-red-600">{{ stats.risque_eleve }}</p><p class="text-xs text-gray-500">Grossesses à risque</p></div>
      </div>
      <div class="stat-card p-4 flex items-center gap-3 border-l-4 border-green-500">
        <div class="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center text-lg">👶</div>
        <div><p class="text-xl font-extrabold text-green-600">{{ stats.accouchements_mois }}</p><p class="text-xs text-gray-500">Accouchements ce mois</p></div>
      </div>
    </div>

    <!-- Tabs -->
    <div class="flex gap-1 bg-gray-100 rounded-lg p-1 w-fit">
      <button v-for="tab in [{k:'grossesses',l:'🤰 Grossesses'},{k:'accouchements',l:'👶 Accouchements'}]" :key="tab.k"
        @click="activeTab = tab.k"
        :class="['px-4 py-2 rounded-md text-sm font-semibold transition-all', activeTab === tab.k ? 'bg-white text-pink-700 shadow-sm' : 'text-gray-500 hover:text-gray-700']">
        {{ tab.l }}
      </button>
    </div>

    <!-- Grossesses -->
    <div v-if="activeTab === 'grossesses'" class="stat-card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="table-header">
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Patiente</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">SA</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Terme prévu</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Type</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Risque</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Consultations</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Médecin</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="g in grossesses" :key="g.id" class="table-row border-b border-gray-50">
              <td class="px-4 py-3">
                <div class="flex items-center gap-2">
                  <div class="w-8 h-8 rounded-full bg-pink-100 flex items-center justify-center text-pink-700 font-bold text-xs">
                    {{ g.patiente.split(' ').map(n=>n[0]).join('') }}
                  </div>
                  <div>
                    <p class="font-semibold text-gray-900">{{ g.patiente }}</p>
                    <p class="text-xs text-gray-400">{{ g.age }} ans · {{ g.groupe }}</p>
                  </div>
                </div>
              </td>
              <td class="px-4 py-3">
                <div class="flex items-center gap-2">
                  <div class="w-full max-w-[80px] bg-gray-100 rounded-full h-2">
                    <div class="h-2 rounded-full bg-pink-400" :style="{width: Math.min(100, g.sa/40*100)+'%'}"></div>
                  </div>
                  <span class="text-sm font-bold text-pink-700">{{ g.sa }} SA</span>
                </div>
              </td>
              <td class="px-4 py-3 text-gray-600">{{ g.terme }}</td>
              <td class="px-4 py-3">
                <span :class="['text-xs font-medium px-2.5 py-1 rounded-full', typeColor[g.type]]">{{ g.type }}</span>
              </td>
              <td class="px-4 py-3">
                <span :class="['text-xs font-medium px-2.5 py-1 rounded-full', risqueColor[g.risque]]">{{ g.risque }}</span>
              </td>
              <td class="px-4 py-3 text-center">
                <span class="text-sm font-bold text-gray-700">{{ g.consultations }}</span>
                <span class="text-xs text-gray-400">/9</span>
              </td>
              <td class="px-4 py-3 text-gray-600">{{ g.medecin }}</td>
              <td class="px-4 py-3">
                <button class="text-pink-600 hover:text-pink-800 text-xs font-medium">Voir →</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Accouchements -->
    <div v-if="activeTab === 'accouchements'" class="stat-card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="table-header">
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Patiente</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Date / Heure</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Type</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Sage-femme</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Nouveau-né</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Apgar</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Statut</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="a in accouchements" :key="a.id" class="table-row border-b border-gray-50">
              <td class="px-4 py-3 font-semibold text-gray-900">{{ a.patiente }}</td>
              <td class="px-4 py-3">
                <p class="text-gray-700">{{ a.date }}</p>
                <p class="text-xs text-gray-400 font-mono">{{ a.heure }}</p>
              </td>
              <td class="px-4 py-3 text-gray-600">{{ a.type }}</td>
              <td class="px-4 py-3 text-gray-600">{{ a.sage_femme }}</td>
              <td class="px-4 py-3">
                <p class="text-sm font-semibold">{{ a.poids }}g · {{ a.sexe === 'M' ? '♂' : '♀' }}</p>
              </td>
              <td class="px-4 py-3">
                <span :class="['text-xs font-bold px-2 py-0.5 rounded-full', a.apgar5 >= 9 ? 'badge-success' : a.apgar5 >= 7 ? 'badge-warning' : 'badge-danger']">
                  {{ a.apgar1 }}/{{ a.apgar5 }}
                </span>
              </td>
              <td class="px-4 py-3">
                <span class="badge-success text-xs font-medium px-2.5 py-1 rounded-full">{{ a.statut }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>
