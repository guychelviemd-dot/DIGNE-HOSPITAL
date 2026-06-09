<script setup>
import { useToastStore } from '@/stores/toast'
const toast = useToastStore()
</script>

<template>
  <RouterView />

  <!-- Toast global -- Violet premium -->
  <Teleport to="body">
    <div class="fixed bottom-6 right-6 z-[200] flex flex-col gap-2 pointer-events-none">
      <transition-group name="toast">
        <div v-for="t in toast.toasts" :key="t.id"
          :class="['flex items-center gap-3 px-4 py-3 rounded-xl shadow-2xl text-sm font-semibold pointer-events-auto border',
            t.type === 'success' ? 'bg-gradient-to-r from-green-600 to-emerald-600 text-white border-green-400' :
            t.type === 'error'   ? 'bg-gradient-to-r from-red-600 to-rose-600 text-white border-red-400' :
            t.type === 'warning' ? 'bg-gradient-to-r from-amber-500 to-orange-500 text-white border-amber-300' :
            'bg-gradient-to-r from-violet-700 to-purple-700 text-white border-violet-500']">
          <span class="text-base">
            {{ t.type === 'success' ? '✅' : t.type === 'error' ? '❌' : t.type === 'warning' ? '⚠️' : 'ℹ️' }}
          </span>
          <span>{{ t.message }}</span>
          <button @click="toast.remove(t.id)" class="ml-2 opacity-70 hover:opacity-100 text-lg leading-none">×</button>
        </div>
      </transition-group>
    </div>
  </Teleport>
</template>

<style>
.toast-enter-active { transition: all 0.3s cubic-bezier(0.4,0,0.2,1); }
.toast-leave-active { transition: all 0.2s ease; }
.toast-enter-from   { opacity: 0; transform: translateX(50px) scale(0.95); }
.toast-leave-to     { opacity: 0; transform: translateX(50px); }
</style>
