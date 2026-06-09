<script setup>
import { ref, computed } from 'vue'

const activeTab = ref('planning')
const showModal = ref(false)

const interventions = ref([
  { id: 1, patient: 'Koné Ibrahim', age: 67, acte: 'Pontage coronarien', ccam: 'DKSA001', chirurgien: 'Dr. Diallo', anesthesiste: 'Dr. Bah', salle: 'Bloc A', heure: '08:00', duree: 180, statut: 'En cours', urgence: 'Urgente', anesthesie: 'Générale' },
  { id: 2, patient: 'Traoré Aminata', age: 28, acte: 'Appendicectomie', ccam: 'HHFA016', chirurgien: 'Dr. Camara', anesthesiste: 'Dr. Sylla', salle: 'Bloc B', heure: '10:30', duree: 60, statut: 'Programmée', urgence: 'Semi-urgente', anesthesie: 'Générale' },
  { id: 3, patient: 'Bah Sekou', age: 52, acte: 'Cholécystectomie laparoscopique', ccam: 'HHFA011', chirurgien: 'Dr. Diallo', anesthesiste: 'Dr. Bah', salle: 'Bloc A', heure: '13:00', duree: 90, statut: 'Programmée', urgence: 'Programmée', anesthesie: 'Générale' },
  { id: 4, patient: 'Sylla Fatoumata', age: 45, acte: 'Prothèse totale hanche', ccam: 'NEKA010', chirurgien: 'Dr. Kouyaté', anesthesiste: 'Dr. Sylla', salle: 'Bloc C', heure: '14:30', duree: 120, statut: 'Terminée', urgence: 'Programmée', anesthesie: 'Rachianesthésie' },
])

const salles = [
  { nom: 'Bloc A', statut: 'Occupé', intervention: 'Pontage coronarien', heure_fin: '11:00' },
  { nom: 'Bloc B', statut: 'Libre', intervention: null, heure_fin: null },
  { nom: 'Bloc C', statut: 'Nettoyage', intervention: null, heure_fin: '14:00' },
  { nom: 'Bloc D', statut: 'Libre', intervention: null, heure_fin: null },
]

const statutColor = {
  'En cours': 'badge-chu', 'Programmée': 'badge-info',
  'Terminée': 'badge-success', 'Annulée': 'badge-danger', 'Reportée': 'badge-warning',
}
const urgenceColor = {
  'Programmée': 'badge-info', 'Semi-urgente': 'badge-warning', 'Urgente': 'badge-danger',
}
const salleStatutColor = {
  'Occupé': 'bg-red-100 text-red-700 border-red-200',
  'Libre': 'bg-green-100 text-green-700 border-green-200',
  'Nettoyage': 'bg-amber-100 text-amber-700 border-amber-200',
}

const stats = computed(() => ({
  en_cours: interventions.value.filter(i => i.statut === 'En cours').length,
  programmees: interventions.value.filter(i => i.statut === 'Programmée').length,
  terminees: interventions.value.filter(i => i.statut === 'Terminée').length,
  salles_libres: salles.filter(s => s.statut === 'Libre').length,
}))
</script>

<template>
  <div class="space-y-5">

    <div class="flex items-center justify-between">
      <div>
        <h2 class="page-title">🔪 Bloc Opératoire</h2>
        <p class="text-sm text-gray-500 mt-0.5">Planning des interventions chirurgicales</p>
      </div>
      <button @click="showModal = true" class="btn-primary">+ Programmer intervention</button>
    </div>

    <!-- KPIs -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
      <div class="stat-card p-4 flex items-center gap-3 border-l-4 border-blue-500">
        <div class="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center text-lg">⚡</div>
        <div><p class="text-xl font-extrabold text-blue-600">{{ stats.en_cours }}</p><p class="text-xs text-gray-500">En cours</p></div>
      </div>
      <div class="stat-card p-4 flex items-center gap-3 border-l-4 border-amber-400">
        <div class="w-10 h-10 rounded-lg bg-amber-100 flex items-center justify-center text-lg">📅</div>
        <div><p class="text-xl font-extrabold text-amber-600">{{ stats.programmees }}</p><p class="text-xs text-gray-500">Programmées</p></div>
      </div>
      <div class="stat-card p-4 flex items-center gap-3 border-l-4 border-green-500">
        <div class="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center text-lg">✅</div>
        <div><p class="text-xl font-extrabold text-green-600">{{ stats.terminees }}</p><p class="text-xs text-gray-500">Terminées</p></div>
      </div>
      <div class="stat-card p-4 flex items-center gap-3 border-l-4 border-teal-500">
        <div class="w-10 h-10 rounded-lg bg-teal-100 flex items-center justify-center text-lg">🏥</div>
        <div><p class="text-xl font-extrabold text-teal-600">{{ stats.salles_libres }}</p><p class="text-xs text-gray-500">Salles libres</p></div>
      </div>
    </div>

    <!-- Statut des salles -->
    <div class="stat-card p-5">
      <p class="section-title mb-4">État des salles d'opération</p>
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div v-for="s in salles" :key="s.nom"
          :class="['p-4 rounded-xl border-2 transition-all', salleStatutColor[s.statut]]">
          <div class="flex items-center justify-between mb-2">
            <p class="font-bold text-sm">{{ s.nom }}</p>
            <span :class="['text-xs font-bold px-2 py-0.5 rounded-full', salleStatutColor[s.statut]]">{{ s.statut }}</span>
          </div>
          <p v-if="s.intervention" class="text-xs font-medium truncate">{{ s.intervention }}</p>
          <p v-if="s.heure_fin" class="text-xs mt-1 opacity-70">Fin prévue: {{ s.heure_fin }}</p>
          <p v-if="!s.intervention" class="text-xs opacity-60">Disponible</p>
        </div>
      </div>
    </div>

    <!-- Planning du jour -->
    <div class="stat-card overflow-hidden">
      <div class="p-4 border-b border-gray-100 flex items-center justify-between">
        <p class="section-title">Planning du jour</p>
        <div class="flex gap-1 bg-gray-100 rounded-lg p-1">
          <button v-for="tab in [{k:'planning',l:'Planning'},{k:'compte-rendus',l:'Comptes-rendus'}]" :key="tab.k"
            @click="activeTab = tab.k"
            :class="['px-3 py-1.5 rounded-md text-xs font-semibold transition-all', activeTab === tab.k ? 'bg-white text-blue-700 shadow-sm' : 'text-gray-500']">
            {{ tab.l }}
          </button>
        </div>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="table-header">
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Heure</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Patient</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Acte (CCAM)</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Chirurgien</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Anesthésie</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Salle</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Durée</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Urgence</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Statut</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="i in interventions" :key="i.id"
              :class="['table-row border-b border-gray-50', i.statut === 'En cours' ? 'bg-blue-50/30' : '']">
              <td class="px-4 py-3 font-mono font-bold text-blue-700">{{ i.heure }}</td>
              <td class="px-4 py-3">
                <p class="font-semibold text-gray-900">{{ i.patient }}</p>
                <p class="text-xs text-gray-400">{{ i.age }} ans</p>
              </td>
              <td class="px-4 py-3">
                <p class="font-medium text-gray-800">{{ i.acte }}</p>
                <p class="text-xs text-gray-400 font-mono">{{ i.ccam }}</p>
              </td>
              <td class="px-4 py-3 text-gray-600">{{ i.chirurgien }}</td>
              <td class="px-4 py-3 text-xs text-gray-600">{{ i.anesthesie }}</td>
              <td class="px-4 py-3">
                <span class="text-xs font-bold bg-blue-100 text-blue-700 px-2 py-0.5 rounded">{{ i.salle }}</span>
              </td>
              <td class="px-4 py-3 text-xs text-gray-600">{{ i.duree }} min</td>
              <td class="px-4 py-3">
                <span :class="['text-xs font-medium px-2 py-0.5 rounded-full', urgenceColor[i.urgence]]">{{ i.urgence }}</span>
              </td>
              <td class="px-4 py-3">
                <span :class="['text-xs font-medium px-2.5 py-1 rounded-full', statutColor[i.statut]]">{{ i.statut }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>
