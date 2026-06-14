import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

export default defineConfig({
  root: '.', // Force Vite à travailler dans le dossier courant
  base: '/', // Assure des chemins absolus pour Nginx
  plugins: [
    vue(),
    tailwindcss()
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    outDir: 'dist', // Spécifie explicitement le nom du dossier de sortie
    emptyOutDir: true // Nettoie le dossier avant chaque build
  }
})