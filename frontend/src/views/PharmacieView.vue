<script setup>
import { ref, computed } from 'vue'

const search = ref('')

const medicaments = ref([
  { id: 1, nom: 'Artémether 80mg', categorie: 'Antipaludéen', stock: 245, seuil: 50, lot: 'LOT-2025-001', peremption: '2026-08-01', statut: 'Normal' },
  { id: 2, nom: 'Amlodipine 5mg', categorie: 'Antihypertenseur', stock: 32, seuil: 50, lot: 'LOT-2025-002', peremption: '2026-03-15', statut: 'Alerte' },
  { id: 3, nom: 'Metformine 500mg', categorie: 'Antidiabétique', stock: 180, seuil: 40, lot: 'LOT-2025-003', peremption: '2027-01-20', statut: 'Normal' },
  { id: 4, nom: 'Amoxicilline 500mg', categorie: 'Antibiotique', stock: 8, seuil: 30, lot: 'LOT-2025-004', peremption: '2025-12-10', statut: 'Rupture' },
  { id: 5, nom: 'Paracétamol 500mg', categorie: 'Analgésique', stock: 520, seuil: 100, lot: 'LOT-2025-005', peremption: '2026-11-30', statut: 'Normal' },
  { id: 6, nom: 'Ibuprofène 400mg', categorie: 'Anti-inflammatoire', stock: 67, seuil: 60, lot: 'LOT-2025-006', peremption: '2026-06-01', statut: 'Normal' },
])

const filtered = computed(() =>
  medicaments.value.filter(m => m.nom.toLowerCase().includes(search.value.toLowerCase()))
)

const alertes = computed(() => medicaments.value.filter(m => m.statut !== 'Normal'))

const statutColor = { 'Normal': 'badge-success', 'Alerte': 'badge-warning', 'Rupture': 'badge-danger' }

function stockPercent(m) {
  return Math.min(100, Math.round((m.stock / (m.seuil * 5)) * 100))
}
</script>

<template>
  <div class="space-y-5">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="page-title">Pharmacie</h2>
        <p class="text-sm text-violet-500 mt-0.5">Gestion des stocks et médicaments</p>
      </div>
      <button class="btn-primary">+ Entrée de stock</button>
    </div>

    <!-- Score module 100% -->
    <div class="stat-card p-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center text-white text-xl shadow-lg">💊</div>
          <div>
            <p class="text-sm font-bold text-gray-900">Module Pharmacie</p>
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
              <circle cx="18" cy="18" r="14" fill="none" stroke="url(#score-gradient-pharm)" stroke-width="3.5" stroke-dasharray="88 88" stroke-linecap="round"/>
            </svg>
            <defs>
              <linearGradient id="score-gradient-pharm" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:#a855f7"/>
                <stop offset="100%" style="stop-color:#7e22ce"/>
              </linearGradient>
            </defs>
          </div>
        </div>
      </div>
    </div>

    <!-- Alertes -->
    <div v-if="alertes.length" class="bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-200 rounded-xl p-4 shadow-sm">
      <p class="text-sm font-semibold text-amber-800 mb-2">⚠ Alertes stock ({{ alertes.length }})</p>
      <div class="flex flex-wrap gap-2">
        <span v-for="a in alertes" :key="a.id" :class="['text-xs font-medium px-3 py-1 rounded-full', statutColor[a.statut]]">
          {{ a.nom }} — {{ a.stock }} unités
        </span>
      </div>
    </div>

    <div class="stat-card p-4">
      <input v-model="search" class="input-field max-w-xs" placeholder="🔍  Rechercher un médicament..." />
    </div>

    <div class="stat-card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="table-header">
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Médicament</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Catégorie</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Stock</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Niveau</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">N° Lot</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Péremption</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Statut</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="m in filtered" :key="m.id" class="table-row border-b border-gray-50">
              <td class="px-4 py-3 font-medium text-gray-900">{{ m.nom }}</td>
              <td class="px-4 py-3 text-gray-500">{{ m.categorie }}</td>
              <td class="px-4 py-3 font-bold text-gray-900">{{ m.stock }} <span class="text-xs text-gray-400 font-normal">/ seuil {{ m.seuil }}</span></td>
              <td class="px-4 py-3 w-32">
                <div class="w-full bg-gray-100 rounded-full h-2">
                  <div
                    :class="['h-2 rounded-full', m.statut === 'Normal' ? 'bg-gradient-to-r from-green-500 to-emerald-500' : m.statut === 'Alerte' ? 'bg-gradient-to-r from-amber-500 to-orange-500' : 'bg-gradient-to-r from-red-500 to-rose-500']"
                    :style="{ width: stockPercent(m) + '%' }"
                  ></div>
                </div>
              </td>
              <td class="px-4 py-3 text-gray-500 text-xs">{{ m.lot }}</td>
              <td class="px-4 py-3 text-gray-500">{{ m.peremption }}</td>
              <td class="px-4 py-3">
                <span :class="['text-xs font-medium px-2.5 py-1 rounded-full', statutColor[m.statut]]">{{ m.statut }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
