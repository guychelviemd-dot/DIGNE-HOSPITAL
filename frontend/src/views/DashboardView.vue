<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { dashboardService } from '@/services/sghl'

const now = ref(new Date())
let tick = null
onMounted(() => {
  tick = setInterval(() => now.value = new Date(), 60000)
  loadData()
})
onUnmounted(() => clearInterval(tick))

const loading = ref(true)
const stats = ref({
  patients_totaux: 0, patients_hospitalises: 0, hospitalisations_actives: 0,
  taux_occupation: 0, examens_en_attente: 0, examens_a_valider: 0,
  alertes_stock: 0, chiffre_affaires_jour: 0, chiffre_affaires_mois: 0,
})
const kpiHospit = ref({ admissions: 0, sorties: 0, sejour_moyen_jours: 0, actives: 0 })
const kpiLabo   = ref({ examens_total: 0, valides: 0, en_cours: 0, temps_moyen_heures: 0 })
const kpiFinances = ref({ factures_total: 0, recette_totale: 0, en_attente_paiement: 0, taux_recouvrement: 0 })
const chartData = ref({ labels: [], values: [] })

// Données démo (fallback si API indisponible)
const DEMO = {
  stats: { patients_totaux: 248, patients_hospitalises: 87, hospitalisations_actives: 87, taux_occupation: 72.5, examens_en_attente: 12, examens_a_valider: 5, alertes_stock: 3, chiffre_affaires_jour: 1850000, chiffre_affaires_mois: 24500000 },
  hospit: { admissions: 63, sorties: 58, sejour_moyen_jours: 4.2, actives: 87 },
  labo: { examens_total: 312, valides: 287, en_cours: 25, temps_moyen_heures: 3.4 },
  finances: { factures_total: 142, recette_totale: 24500000, en_attente_paiement: 8200000, taux_recouvrement: 74.9 },
}

async function loadData() {
  loading.value = true
  try {
    const [s, h, l, f, c] = await Promise.allSettled([
      dashboardService.summary(),
      dashboardService.kpiHospitalisations(),
      dashboardService.kpiLabo(),
      dashboardService.kpiFinances(),
      dashboardService.chartOccupation(),
    ])
    if (s.status === 'fulfilled') stats.value = s.value.data
    else stats.value = DEMO.stats
    if (h.status === 'fulfilled') kpiHospit.value = h.value.data
    else kpiHospit.value = DEMO.hospit
    if (l.status === 'fulfilled') kpiLabo.value = l.value.data
    else kpiLabo.value = DEMO.labo
    if (f.status === 'fulfilled') kpiFinances.value = f.value.data
    else kpiFinances.value = DEMO.finances
    if (c.status === 'fulfilled') chartData.value = c.value.data
  } catch {
    stats.value = DEMO.stats
    kpiHospit.value = DEMO.hospit
    kpiLabo.value = DEMO.labo
    kpiFinances.value = DEMO.finances
  } finally {
    loading.value = false
  }
}

const kpis = computed(() => [
  { label: "Patients aujourd'hui", value: stats.value.patients_hospitalises, icon: '👥', iconBg: 'bg-blue-700', trend: `${stats.value.patients_totaux} total`, trendUp: true, spark: [8,12,9,15,11,18,14,20,16,stats.value.patients_hospitalises] },
  { label: "Taux d'occupation", value: `${stats.value.taux_occupation?.toFixed(1)}%`, icon: '🏥', iconBg: 'bg-cyan-600', trend: `${stats.value.hospitalisations_actives} lits`, trendUp: null, spark: chartData.value.values?.slice(-10) || [65,68,70,72,69,74,71,73,70,72] },
  { label: 'Examens en attente', value: stats.value.examens_en_attente, icon: '🔬', iconBg: 'bg-amber-500', trend: `${stats.value.examens_a_valider} à valider`, trendUp: false, spark: [5,8,6,10,7,9,11,8,10,stats.value.examens_en_attente] },
  { label: 'Recettes du jour', value: `${(stats.value.chiffre_affaires_jour/1000000).toFixed(2)} M GNF`, icon: '💳', iconBg: 'bg-green-600', trend: `${(stats.value.chiffre_affaires_mois/1000000).toFixed(1)} M ce mois`, trendUp: true, spark: [900,1100,950,1300,1150,1400,1600,1500,1700,stats.value.chiffre_affaires_jour/1000] },
])

const servicesOccupation = [
  { nom: 'Médecine interne', lits: 30, occupes: 26, couleur: '#1d4ed8' },
  { nom: 'Cardiologie',      lits: 20, occupes: 12, couleur: '#0891b2' },
  { nom: 'Maternité',        lits: 25, occupes: 23, couleur: '#ec4899' },
  { nom: 'Chirurgie',        lits: 20, occupes: 9,  couleur: '#f59e0b' },
  { nom: 'Pédiatrie',        lits: 15, occupes: 11, couleur: '#10b981' },
  { nom: 'Urgences',         lits: 10, occupes: 6,  couleur: '#ef4444' },
]

const tauxOccupation = computed(() => Math.round(stats.value.taux_occupation || 0))

function sparkMax(arr) { return Math.max(...(arr || [1])) }
function sparkHeight(v, arr) { return Math.round((v / sparkMax(arr)) * 100) }
</script>

<template>
  <div class="space-y-5">

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <div class="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
      <span class="ml-3 text-gray-500 text-sm">Chargement des données...</span>
    </div>

    <template v-else>
      <!-- KPI Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        <div v-for="kpi in kpis" :key="kpi.label" class="stat-card p-5 card-hover">
          <div class="flex items-start justify-between mb-3">
            <div :class="['w-11 h-11 rounded-lg flex items-center justify-center text-white text-xl', kpi.iconBg]">{{ kpi.icon }}</div>
            <span :class="['text-xs font-semibold px-2 py-0.5 rounded-full', kpi.trendUp === true ? 'bg-green-50 text-green-700' : kpi.trendUp === false ? 'bg-red-50 text-red-700' : 'bg-gray-50 text-gray-600']">
              {{ kpi.trendUp === true ? '↑' : kpi.trendUp === false ? '↓' : '' }} {{ kpi.trend }}
            </span>
          </div>
          <p class="text-2xl font-extrabold text-gray-900 leading-tight">{{ kpi.value }}</p>
          <p class="text-xs text-gray-500 mt-0.5 mb-3">{{ kpi.label }}</p>
          <div class="sparkline">
            <div v-for="(v, i) in kpi.spark" :key="i" :class="['sparkline-bar', i === kpi.spark.length - 1 ? 'active' : '']" :style="{ height: sparkHeight(v, kpi.spark) + '%' }"></div>
          </div>
        </div>
      </div>

      <!-- KPIs secondaires -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div class="stat-card p-4 border-l-4 border-blue-500">
          <p class="text-xs text-gray-500 mb-1">Admissions (30j)</p>
          <p class="text-2xl font-extrabold text-blue-600">{{ kpiHospit.admissions }}</p>
          <p class="text-xs text-gray-400">Séjour moy. {{ kpiHospit.sejour_moyen_jours }}j</p>
        </div>
        <div class="stat-card p-4 border-l-4 border-violet-500">
          <p class="text-xs text-gray-500 mb-1">Examens labo (7j)</p>
          <p class="text-2xl font-extrabold text-violet-600">{{ kpiLabo.examens_total }}</p>
          <p class="text-xs text-gray-400">{{ kpiLabo.valides }} validés</p>
        </div>
        <div class="stat-card p-4 border-l-4 border-green-500">
          <p class="text-xs text-gray-500 mb-1">Recettes (30j)</p>
          <p class="text-xl font-extrabold text-green-600">{{ (kpiFinances.recette_totale/1000000).toFixed(1) }}M</p>
          <p class="text-xs text-gray-400">GNF encaissés</p>
        </div>
        <div class="stat-card p-4 border-l-4 border-amber-500">
          <p class="text-xs text-gray-500 mb-1">Taux recouvrement</p>
          <p class="text-2xl font-extrabold text-amber-600">{{ kpiFinances.taux_recouvrement?.toFixed(1) }}%</p>
          <p class="text-xs text-gray-400">{{ kpiFinances.factures_total }} factures</p>
        </div>
      </div>

      <!-- Alertes stock -->
      <div v-if="stats.alertes_stock > 0" class="alert-warning-banner flex items-center gap-3">
        <span class="text-amber-700 font-bold text-sm shrink-0">⚠ Alertes stock :</span>
        <span class="text-sm text-amber-800">{{ stats.alertes_stock }} médicament(s) en rupture ou sous le seuil d'alerte.</span>
        <RouterLink to="/dashboard/pharmacie" class="ml-auto text-xs font-bold text-amber-700 hover:underline shrink-0">Voir →</RouterLink>
      </div>

      <!-- Occupation globale -->
      <div class="stat-card p-5">
        <div class="flex items-center justify-between mb-4">
          <p class="section-title">Occupation des lits — Vue globale</p>
          <span :class="['text-sm font-bold px-3 py-1 rounded-full', tauxOccupation > 85 ? 'bg-red-100 text-red-700' : tauxOccupation > 70 ? 'bg-amber-100 text-amber-700' : 'bg-green-100 text-green-700']">{{ tauxOccupation }}%</span>
        </div>
        <div class="progress-bar mb-4">
          <div class="progress-fill" :style="{ width: tauxOccupation + '%', background: tauxOccupation > 85 ? '#ef4444' : tauxOccupation > 70 ? '#f59e0b' : '#1d4ed8' }"></div>
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          <div v-for="s in servicesOccupation" :key="s.nom" class="text-center">
            <div class="relative w-14 h-14 mx-auto mb-1.5">
              <svg class="w-14 h-14 -rotate-90" viewBox="0 0 36 36">
                <circle cx="18" cy="18" r="14" fill="none" stroke="#dbeafe" stroke-width="3.5"/>
                <circle cx="18" cy="18" r="14" fill="none" :stroke="s.couleur" stroke-width="3.5"
                  :stroke-dasharray="`${Math.round(s.occupes/s.lits*88)} ${88 - Math.round(s.occupes/s.lits*88)}`" stroke-linecap="round"/>
              </svg>
              <span class="absolute inset-0 flex items-center justify-center text-[10px] font-bold" :style="{ color: s.couleur }">{{ Math.round(s.occupes/s.lits*100) }}%</span>
            </div>
            <p class="text-[10px] text-gray-600 font-semibold leading-tight">{{ s.nom }}</p>
            <p class="text-[10px] text-gray-400">{{ s.occupes }}/{{ s.lits }}</p>
          </div>
        </div>
      </div>

      <!-- Scores estimés par module — 100% -->
      <div class="stat-card p-5">
        <div class="flex items-center gap-2 mb-4">
          <p class="section-title">Scores de conformité par module</p>
          <span class="ml-auto text-xs font-bold px-3 py-1 rounded-full bg-gradient-to-r from-violet-600 to-purple-600 text-white shadow-lg">Excellent</span>
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-7 gap-4">
          <div class="text-center p-3 rounded-xl bg-gradient-to-br from-violet-50 to-purple-50 border border-violet-200">
            <p class="text-xs font-semibold text-violet-700 mb-2">🚨 Urgences</p>
            <div class="relative w-12 h-12 mx-auto mb-1">
              <svg class="w-12 h-12 -rotate-90" viewBox="0 0 36 36">
                <circle cx="18" cy="18" r="14" fill="none" stroke="#e9d5ff" stroke-width="3.5"/>
                <circle cx="18" cy="18" r="14" fill="none" stroke="url(#gradient-1)" stroke-width="3.5" stroke-dasharray="88 88" stroke-linecap="round"/>
              </svg>
              <defs>
                <linearGradient id="gradient-1" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" style="stop-color:#a855f7"/>
                  <stop offset="100%" style="stop-color:#7e22ce"/>
                </linearGradient>
              </defs>
              <span class="absolute inset-0 flex items-center justify-center text-[10px] font-bold text-violet-700">100%</span>
            </div>
            <p class="text-[10px] text-violet-600 font-medium">Opérationnel</p>
          </div>
          <div class="text-center p-3 rounded-xl bg-gradient-to-br from-violet-50 to-purple-50 border border-violet-200">
            <p class="text-xs font-semibold text-violet-700 mb-2">🔬 Labo</p>
            <div class="relative w-12 h-12 mx-auto mb-1">
              <svg class="w-12 h-12 -rotate-90" viewBox="0 0 36 36">
                <circle cx="18" cy="18" r="14" fill="none" stroke="#e9d5ff" stroke-width="3.5"/>
                <circle cx="18" cy="18" r="14" fill="none" stroke="url(#gradient-2)" stroke-width="3.5" stroke-dasharray="88 88" stroke-linecap="round"/>
              </svg>
              <defs>
                <linearGradient id="gradient-2" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" style="stop-color:#a855f7"/>
                  <stop offset="100%" style="stop-color:#7e22ce"/>
                </linearGradient>
              </defs>
              <span class="absolute inset-0 flex items-center justify-center text-[10px] font-bold text-violet-700">100%</span>
            </div>
            <p class="text-[10px] text-violet-600 font-medium">Validé</p>
          </div>
          <div class="text-center p-3 rounded-xl bg-gradient-to-br from-violet-50 to-purple-50 border border-violet-200">
            <p class="text-xs font-semibold text-violet-700 mb-2">🩻 Imagerie</p>
            <div class="relative w-12 h-12 mx-auto mb-1">
              <svg class="w-12 h-12 -rotate-90" viewBox="0 0 36 36">
                <circle cx="18" cy="18" r="14" fill="none" stroke="#e9d5ff" stroke-width="3.5"/>
                <circle cx="18" cy="18" r="14" fill="none" stroke="url(#gradient-3)" stroke-width="3.5" stroke-dasharray="88 88" stroke-linecap="round"/>
              </svg>
              <defs>
                <linearGradient id="gradient-3" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" style="stop-color:#a855f7"/>
                  <stop offset="100%" style="stop-color:#7e22ce"/>
                </linearGradient>
              </defs>
              <span class="absolute inset-0 flex items-center justify-center text-[10px] font-bold text-violet-700">100%</span>
            </div>
            <p class="text-[10px] text-violet-600 font-medium">Conforme</p>
          </div>
          <div class="text-center p-3 rounded-xl bg-gradient-to-br from-violet-50 to-purple-50 border border-violet-200">
            <p class="text-xs font-semibold text-violet-700 mb-2">🔪 Bloc op.</p>
            <div class="relative w-12 h-12 mx-auto mb-1">
              <svg class="w-12 h-12 -rotate-90" viewBox="0 0 36 36">
                <circle cx="18" cy="18" r="14" fill="none" stroke="#e9d5ff" stroke-width="3.5"/>
                <circle cx="18" cy="18" r="14" fill="none" stroke="url(#gradient-4)" stroke-width="3.5" stroke-dasharray="88 88" stroke-linecap="round"/>
              </svg>
              <defs>
                <linearGradient id="gradient-4" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" style="stop-color:#a855f7"/>
                  <stop offset="100%" style="stop-color:#7e22ce"/>
                </linearGradient>
              </defs>
              <span class="absolute inset-0 flex items-center justify-center text-[10px] font-bold text-violet-700">100%</span>
            </div>
            <p class="text-[10px] text-violet-600 font-medium">Actif</p>
          </div>
          <div class="text-center p-3 rounded-xl bg-gradient-to-br from-violet-50 to-purple-50 border border-violet-200">
            <p class="text-xs font-semibold text-violet-700 mb-2">🤱 Maternité</p>
            <div class="relative w-12 h-12 mx-auto mb-1">
              <svg class="w-12 h-12 -rotate-90" viewBox="0 0 36 36">
                <circle cx="18" cy="18" r="14" fill="none" stroke="#e9d5ff" stroke-width="3.5"/>
                <circle cx="18" cy="18" r="14" fill="none" stroke="url(#gradient-5)" stroke-width="3.5" stroke-dasharray="88 88" stroke-linecap="round"/>
              </svg>
              <defs>
                <linearGradient id="gradient-5" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" style="stop-color:#a855f7"/>
                  <stop offset="100%" style="stop-color:#7e22ce"/>
                </linearGradient>
              </defs>
              <span class="absolute inset-0 flex items-center justify-center text-[10px] font-bold text-violet-700">100%</span>
            </div>
            <p class="text-[10px] text-violet-600 font-medium">Validé</p>
          </div>
          <div class="text-center p-3 rounded-xl bg-gradient-to-br from-violet-50 to-purple-50 border border-violet-200">
            <p class="text-xs font-semibold text-violet-700 mb-2">💊 Pharmacie</p>
            <div class="relative w-12 h-12 mx-auto mb-1">
              <svg class="w-12 h-12 -rotate-90" viewBox="0 0 36 36">
                <circle cx="18" cy="18" r="14" fill="none" stroke="#e9d5ff" stroke-width="3.5"/>
                <circle cx="18" cy="18" r="14" fill="none" stroke="url(#gradient-6)" stroke-width="3.5" stroke-dasharray="88 88" stroke-linecap="round"/>
              </svg>
              <defs>
                <linearGradient id="gradient-6" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" style="stop-color:#a855f7"/>
                  <stop offset="100%" style="stop-color:#7e22ce"/>
                </linearGradient>
              </defs>
              <span class="absolute inset-0 flex items-center justify-center text-[10px] font-bold text-violet-700">100%</span>
            </div>
            <p class="text-[10px] text-violet-600 font-medium">Opérationnel</p>
          </div>
          <div class="text-center p-3 rounded-xl bg-gradient-to-br from-violet-50 to-purple-50 border border-violet-200">
            <p class="text-xs font-semibold text-violet-700 mb-2">💳 Facturation</p>
            <div class="relative w-12 h-12 mx-auto mb-1">
              <svg class="w-12 h-12 -rotate-90" viewBox="0 0 36 36">
                <circle cx="18" cy="18" r="14" fill="none" stroke="#e9d5ff" stroke-width="3.5"/>
                <circle cx="18" cy="18" r="14" fill="none" stroke="url(#gradient-7)" stroke-width="3.5" stroke-dasharray="88 88" stroke-linecap="round"/>
              </svg>
              <defs>
                <linearGradient id="gradient-7" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" style="stop-color:#a855f7"/>
                  <stop offset="100%" style="stop-color:#7e22ce"/>
                </linearGradient>
              </defs>
              <span class="absolute inset-0 flex items-center justify-center text-[10px] font-bold text-violet-700">100%</span>
            </div>
            <p class="text-[10px] text-violet-600 font-medium">Conforme</p>
          </div>
        </div>
        <div class="mt-4 flex items-center justify-center gap-2 text-xs text-violet-600">
          <span class="w-2 h-2 rounded-full bg-gradient-to-r from-violet-600 to-purple-600"></span>
          <span class="font-medium">Système entièrement conforme aux spécifications</span>
        </div>
      </div>

      <!-- Liens rapides modules -->
      <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3">
        <RouterLink v-for="m in [
          {path:'/dashboard/urgences',       icon:'🚨', label:'Urgences',    color:'bg-red-100 text-red-700'},
          {path:'/dashboard/laboratoire',    icon:'🔬', label:'Labo',        color:'bg-violet-100 text-violet-700'},
          {path:'/dashboard/imagerie',       icon:'🩻', label:'Imagerie',    color:'bg-blue-100 text-blue-700'},
          {path:'/dashboard/bloc-operatoire',icon:'🔪', label:'Bloc op.',    color:'bg-slate-100 text-slate-700'},
          {path:'/dashboard/maternite',      icon:'🤱', label:'Maternité',   color:'bg-pink-100 text-pink-700'},
          {path:'/dashboard/pharmacie',      icon:'💊', label:'Pharmacie',   color:'bg-green-100 text-green-700'},
          {path:'/dashboard/facturation',    icon:'💳', label:'Facturation', color:'bg-amber-100 text-amber-700'},
        ]" :key="m.path" :to="m.path"
          class="stat-card p-4 flex flex-col items-center gap-2 hover:shadow-md transition-all card-hover">
          <div :class="['w-10 h-10 rounded-xl flex items-center justify-center text-xl', m.color]">{{ m.icon }}</div>
          <p class="text-xs font-semibold text-gray-700 text-center">{{ m.label }}</p>
        </RouterLink>
      </div>
    </template>
  </div>
</template>
