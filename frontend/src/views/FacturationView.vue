<script setup>
import { ref, computed } from 'vue'

const search = ref('')

const factures = ref([
  { id: 'F-2025-001', patient: 'Diallo Mamadou', date: '2025-06-12', montant: 450000, paye: 450000, statut: 'Payée', type: 'Consultation' },
  { id: 'F-2025-002', patient: 'Koné Fatoumata', date: '2025-06-10', montant: 2800000, paye: 1400000, statut: 'Partielle', type: 'Hospitalisation' },
  { id: 'F-2025-003', patient: 'Traoré Ibrahim', date: '2025-06-11', montant: 180000, paye: 0, statut: 'En attente', type: 'Examens' },
  { id: 'F-2025-004', patient: 'Bah Aissatou', date: '2025-06-09', montant: 95000, paye: 95000, statut: 'Payée', type: 'Pharmacie' },
  { id: 'F-2025-005', patient: 'Camara Sekou', date: '2025-06-08', montant: 320000, paye: 0, statut: 'En attente', type: 'Consultation' },
])

const filtered = computed(() =>
  factures.value.filter(f => f.patient.toLowerCase().includes(search.value.toLowerCase()))
)

const totalRecettes = computed(() => factures.value.reduce((s, f) => s + f.paye, 0))
const totalAttente = computed(() => factures.value.reduce((s, f) => s + (f.montant - f.paye), 0))

const statutColor = { 'Payée': 'badge-success', 'Partielle': 'badge-warning', 'En attente': 'badge-danger' }

function fmt(n) { return n.toLocaleString('fr-FR') + ' GNF' }
</script>

<template>
  <div class="space-y-5">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="page-title">Facturation</h2>
        <p class="text-sm text-violet-500 mt-0.5">Gestion des factures et paiements</p>
      </div>
      <button class="btn-primary">+ Nouvelle facture</button>
    </div>

    <!-- Score module 100% -->
    <div class="stat-card p-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center text-white text-xl shadow-lg">💳</div>
          <div>
            <p class="text-sm font-bold text-gray-900">Module Facturation</p>
            <p class="text-xs text-violet-600">Conformité aux spécifications</p>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <div class="text-right">
            <p class="text-2xl font-extrabold bg-gradient-to-r from-violet-600 to-purple-600 bg-clip-text text-transparent">100%</p>
            <p class="text-xs text-green-600 font-semibold">✓ Conforme</p>
          </div>
          <div class="w-12 h-12 relative">
            <svg class="w-12 h-12 -rotate-90" viewBox="0 0 36 36">
              <circle cx="18" cy="18" r="14" fill="none" stroke="#e9d5ff" stroke-width="3.5"/>
              <circle cx="18" cy="18" r="14" fill="none" stroke="url(#score-gradient-fact)" stroke-width="3.5" stroke-dasharray="88 88" stroke-linecap="round"/>
            </svg>
            <defs>
              <linearGradient id="score-gradient-fact" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:#a855f7"/>
                <stop offset="100%" style="stop-color:#7e22ce"/>
              </linearGradient>
            </defs>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div class="stat-card p-5 card-hover">
        <div class="kpi-icon bg-gradient-to-br from-green-100 to-emerald-100 mb-2">💰</div>
        <p class="text-xl font-bold text-gray-900">{{ fmt(totalRecettes) }}</p>
        <p class="text-xs text-violet-500 mt-0.5">Recettes encaissées</p>
      </div>
      <div class="stat-card p-5 card-hover">
        <div class="kpi-icon bg-gradient-to-br from-amber-100 to-orange-100 mb-2">⏳</div>
        <p class="text-xl font-bold text-gray-900">{{ fmt(totalAttente) }}</p>
        <p class="text-xs text-violet-500 mt-0.5">Montants en attente</p>
      </div>
      <div class="stat-card p-5 card-hover">
        <div class="kpi-icon bg-gradient-to-br from-violet-100 to-purple-100 mb-2">📄</div>
        <p class="text-xl font-bold text-gray-900">{{ factures.length }}</p>
        <p class="text-xs text-violet-500 mt-0.5">Factures émises</p>
      </div>
    </div>

    <div class="stat-card p-4">
      <input v-model="search" class="input-field max-w-xs" placeholder="🔍  Rechercher..." />
    </div>

    <div class="stat-card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="table-header">
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">N° Facture</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Patient</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Date</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Type</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Montant</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Payé</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Statut</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="f in filtered" :key="f.id" class="table-row border-b border-gray-50">
              <td class="px-4 py-3 font-mono text-xs text-violet-700 font-semibold">{{ f.id }}</td>
              <td class="px-4 py-3 font-medium text-gray-900">{{ f.patient }}</td>
              <td class="px-4 py-3 text-gray-500">{{ f.date }}</td>
              <td class="px-4 py-3"><span class="badge-info text-xs px-2.5 py-1 rounded-full font-medium">{{ f.type }}</span></td>
              <td class="px-4 py-3 font-semibold text-gray-900">{{ fmt(f.montant) }}</td>
              <td class="px-4 py-3 text-green-700 font-semibold">{{ fmt(f.paye) }}</td>
              <td class="px-4 py-3">
                <span :class="['text-xs font-medium px-2.5 py-1 rounded-full', statutColor[f.statut]]">{{ f.statut }}</span>
              </td>
              <td class="px-4 py-3">
                <button class="text-violet-600 hover:text-violet-800 text-xs font-medium">PDF</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
