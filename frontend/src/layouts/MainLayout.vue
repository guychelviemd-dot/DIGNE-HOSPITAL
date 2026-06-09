<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const sidebarOpen = ref(true)
const showNotifPanel = ref(false)
const currentTime = ref(new Date())

let clockInterval = null
onMounted(() => { clockInterval = setInterval(() => { currentTime.value = new Date() }, 1000) })
onUnmounted(() => clearInterval(clockInterval))

const timeStr = computed(() => currentTime.value.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' }))
const dateStr = computed(() => currentTime.value.toLocaleDateString('fr-FR', { weekday: 'short', day: 'numeric', month: 'short' }))

const alertesCritiques = ref([
  { id: 1, type: 'danger',  msg: 'Rupture stock : Amoxicilline 500mg',        time: '09:42' },
  { id: 2, type: 'warning', msg: 'Examen urgent en attente : NFS — Diallo M.', time: '10:05' },
  { id: 3, type: 'info',    msg: 'Résultats validés disponibles : Koné F.',    time: '10:18' },
])

const notifications = ref([
  { id: 1, icon: '🔬', title: 'Résultat validé',      desc: 'NFS — Diallo Mamadou',          time: 'Il y a 5 min',  lu: false },
  { id: 2, icon: '💊', title: 'Alerte stock',          desc: 'Amoxicilline < seuil critique', time: 'Il y a 18 min', lu: false },
  { id: 3, icon: '🏥', title: 'Nouvelle admission',    desc: 'Bah Aissatou — Maternité',      time: 'Il y a 32 min', lu: true },
  { id: 4, icon: '📋', title: 'Consultation terminée', desc: 'Dr. Camara — Traoré I.',        time: 'Il y a 1h',     lu: true },
])

const unreadCount = computed(() => notifications.value.filter(n => !n.lu).length)

const navGroups = [
  {
    label: 'Clinique',
    items: [
      { name: 'Tableau de bord',  path: '/dashboard/accueil',         icon: '📊', badge: null },
      { name: 'Patients',         path: '/dashboard/patients',         icon: '👥', badge: null },
      { name: 'Consultations',    path: '/dashboard/consultations',    icon: '🩺', badge: 3 },
      { name: 'Hospitalisations', path: '/dashboard/hospitalisations', icon: '🏥', badge: null },
      { name: 'Soins infirmiers', path: '/dashboard/soins',            icon: '💉', badge: 2 },
      { name: 'Urgences',         path: '/dashboard/urgences',         icon: '🚨', badge: 4 },
      { name: 'Bloc opératoire',  path: '/dashboard/bloc-operatoire',  icon: '🔪', badge: null },
      { name: 'Maternité',        path: '/dashboard/maternite',        icon: '🤱', badge: null },
      { name: 'Téléconsultation', path: '/dashboard/teleconsultation', icon: '📹', badge: null },
    ]
  },
  {
    label: 'Laboratoire & Imagerie',
    items: [
      { name: 'Laboratoire', path: '/dashboard/laboratoire', icon: '🔬', badge: 5 },
      { name: 'Imagerie',    path: '/dashboard/imagerie',    icon: '🩻', badge: null },
      { name: 'Pharmacie',   path: '/dashboard/pharmacie',   icon: '💊', badge: null },
    ]
  },
  {
    label: 'Administration',
    items: [
      { name: 'Facturation', path: '/dashboard/facturation', icon: '💳', badge: null },
      { name: 'Personnel',   path: '/dashboard/personnel',   icon: '👨⚕️', badge: null },
      { name: 'Planning',    path: '/dashboard/planning',    icon: '📅', badge: null },
      { name: 'Rapports',    path: '/dashboard/rapports',    icon: '📈', badge: null },
      { name: 'Paramètres',  path: '/dashboard/parametres',  icon: '⚙️', badge: null },
    ]
  }
]

const userInitials = computed(() => {
  const u = auth.user
  if (!u) return 'AD'
  return ((u.first_name?.[0] || '') + (u.last_name?.[0] || '')).toUpperCase() || 'AD'
})

function logout() {
  localStorage.removeItem('sghl_token')
  localStorage.removeItem('sghl_user')
  window.location.href = '/'
}
function markAllRead() { notifications.value.forEach(n => n.lu = true) }
</script>

<template>
  <div class="flex h-screen overflow-hidden" style="background:#f4f7fb">

    <!-- Sidebar — Violet sombre premium -->
    <aside
      class="sidebar-gradient flex flex-col scrollbar-thin overflow-y-auto transition-all duration-300 shrink-0 z-30"
      :style="{ width: sidebarOpen ? '260px' : '68px' }"
    >
      <!-- Logo -->
      <div class="relative flex items-center gap-3 px-4 py-4 border-b border-white/10">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-violet-500/30 to-purple-600/30 backdrop-blur-sm flex items-center justify-center shrink-0 border border-violet-400/30">
          <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
          </svg>
        </div>
        <transition name="fade">
          <div v-if="sidebarOpen" class="flex-1 min-w-0">
            <p class="text-white font-bold text-sm leading-tight tracking-wide">DIGNE HOSPITAL</p>
            <p class="text-violet-300 text-xs truncate">Espace Professionnel</p>
          </div>
        </transition>
        <button @click="sidebarOpen = !sidebarOpen" class="text-violet-300 hover:text-white transition-colors shrink-0">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
          </svg>
        </button>
      </div>

      <!-- Status -->
      <div v-if="sidebarOpen" class="mx-3 mt-3 mb-1 px-3 py-2 rounded-xl bg-gradient-to-r from-green-500/20 to-emerald-500/20 border border-green-400/30 flex items-center gap-2 shadow-lg">
        <span class="w-2 h-2 rounded-full bg-green-400 pulse-dot shrink-0"></span>
        <span class="text-green-200 text-xs font-medium">Système opérationnel</span>
      </div>

      <!-- Nav -->
      <nav class="flex-1 px-2 py-3 space-y-4">
        <div v-for="group in navGroups" :key="group.label">
          <p v-if="sidebarOpen" class="text-violet-300/50 text-[10px] font-bold uppercase tracking-widest px-2 mb-1.5">{{ group.label }}</p>
          <div class="space-y-0.5">
            <RouterLink
              v-for="item in group.items"
              :key="item.path"
              :to="item.path"
              class="nav-item group"
              :class="{ active: route.path === item.path }"
              :title="!sidebarOpen ? item.name : ''"
            >
              <span class="text-base shrink-0 group-hover:scale-110 transition-transform">{{ item.icon }}</span>
              <span v-if="sidebarOpen" class="truncate flex-1">{{ item.name }}</span>
              <span v-if="sidebarOpen && item.badge"
                class="ml-auto bg-gradient-to-r from-violet-600 to-purple-600 text-white text-[10px] font-bold px-2 py-0.5 rounded-full min-w-[20px] text-center shadow-lg">
                {{ item.badge }}
              </span>
            </RouterLink>
          </div>
        </div>
      </nav>

      <!-- User -->
      <div class="px-3 py-3 border-t border-white/10">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-full bg-gradient-to-br from-violet-600 to-purple-600 flex items-center justify-center text-white font-bold text-sm shrink-0 ring-2 ring-violet-400/40 shadow-lg">
            {{ userInitials }}
          </div>
          <div v-if="sidebarOpen" class="flex-1 min-w-0">
            <p class="text-white text-sm font-semibold truncate">{{ auth.user?.full_name || 'Administrateur' }}</p>
            <p class="text-violet-300 text-xs truncate">{{ auth.user?.role || 'Admin' }}</p>
          </div>
          <button v-if="sidebarOpen" @click="logout" class="text-violet-300 hover:text-red-300 transition-colors" title="Déconnexion">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
          </button>
        </div>
      </div>
    </aside>

    <!-- Main -->
    <div class="flex-1 flex flex-col overflow-hidden">

      <!-- Topbar -->
      <header class="bg-gradient-to-r from-white to-violet-50/50 border-b border-violet-200/50 px-6 py-3 flex items-center justify-between shrink-0 shadow-sm">
        <div>
          <h1 class="page-title text-base leading-tight">{{ route.meta.title || route.name }}</h1>
          <p class="text-xs text-violet-500">{{ dateStr }}</p>
        </div>

        <div class="flex items-center gap-2">
          <!-- Clock -->
          <div class="hidden sm:flex items-center gap-1.5 bg-gradient-to-r from-violet-100 to-purple-100 px-3 py-1.5 rounded-xl border border-violet-200">
            <svg class="w-3.5 h-3.5 text-violet-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <span class="text-xs font-bold text-violet-700 tabular-nums">{{ timeStr }}</span>
          </div>

          <!-- Alertes -->
          <div v-if="alertesCritiques.length" class="hidden md:flex items-center gap-1.5 bg-gradient-to-r from-red-50 to-rose-50 border border-red-200 px-3 py-1.5 rounded-xl shadow-sm">
            <span class="w-2 h-2 rounded-full bg-red-500 pulse-dot"></span>
            <span class="text-xs font-semibold text-red-700">{{ alertesCritiques.length }} alerte(s)</span>
          </div>

          <!-- Notifications -->
          <div class="relative">
            <button @click="showNotifPanel = !showNotifPanel"
              class="relative p-2 rounded-xl hover:bg-violet-100/60 transition-colors">
              <svg class="w-5 h-5 text-violet-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
              </svg>
              <span v-if="unreadCount" class="notif-badge bg-gradient-to-r from-violet-600 to-purple-600">{{ unreadCount }}</span>
            </button>

            <transition name="slide-up">
              <div v-if="showNotifPanel"
                class="absolute right-0 top-11 w-80 bg-white rounded-2xl shadow-xl border border-violet-200 z-50 overflow-hidden">
                <div class="flex items-center justify-between px-4 py-3 border-b border-violet-100">
                  <p class="font-bold text-gray-900 text-sm">Notifications</p>
                  <button @click="markAllRead" class="text-xs text-violet-600 font-medium hover:underline">Tout marquer lu</button>
                </div>
                <div class="max-h-72 overflow-y-auto">
                  <div v-for="n in notifications" :key="n.id"
                    :class="['flex items-start gap-3 px-4 py-3 border-b border-gray-50 hover:bg-violet-50/40 transition-colors',
                      !n.lu ? 'bg-violet-50/30' : '']">
                    <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-violet-100 to-purple-100 flex items-center justify-center text-sm shrink-0">{{ n.icon }}</div>
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-semibold text-gray-900">{{ n.title }}</p>
                      <p class="text-xs text-gray-500 truncate">{{ n.desc }}</p>
                      <p class="text-xs text-gray-400 mt-0.5">{{ n.time }}</p>
                    </div>
                    <div v-if="!n.lu" class="w-2.5 h-2.5 rounded-full bg-gradient-to-r from-violet-600 to-purple-600 mt-1.5 shrink-0 shadow-lg"></div>
                  </div>
                </div>
              </div>
            </transition>
          </div>

          <!-- Avatar -->
          <div class="w-8 h-8 rounded-full bg-gradient-to-br from-violet-600 to-purple-600 flex items-center justify-center text-white text-sm font-bold ring-2 ring-violet-300 shadow-lg">
            {{ userInitials }}
          </div>
        </div>
      </header>

      <!-- Alertes banner -->
      <div v-if="alertesCritiques.length" class="bg-gradient-to-r from-red-50 to-rose-50 border-b border-red-200 px-6 py-2 flex items-center gap-3 overflow-x-auto shrink-0">
        <span class="text-red-700 font-bold text-xs shrink-0">🚨 ALERTES :</span>
        <div class="flex gap-2">
          <span v-for="a in alertesCritiques" :key="a.id"
            :class="['text-xs font-medium px-3 py-1.5 rounded-full shrink-0 border',
              a.type === 'danger'  ? 'bg-gradient-to-r from-red-100 to-rose-100 text-red-800 border-red-200' :
              a.type === 'warning' ? 'bg-gradient-to-r from-amber-100 to-orange-100 text-amber-800 border-amber-200' : 'bg-gradient-to-r from-blue-100 to-violet-100 text-blue-800 border-blue-200']">
            {{ a.msg }}
          </span>
        </div>
      </div>

      <!-- Page -->
      <main class="flex-1 overflow-y-auto p-6">
        <RouterView />
      </main>
    </div>

    <div v-if="showNotifPanel" class="fixed inset-0 z-40" @click="showNotifPanel = false"></div>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
.slide-up-enter-active { transition: all 0.2s cubic-bezier(0.4,0,0.2,1); }
.slide-up-enter-from { opacity: 0; transform: translateY(-8px); }
</style>
