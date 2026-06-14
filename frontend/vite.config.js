import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite' // <-- On importe le compilateur v4
import path from 'path'

export default defineConfig({
  base: '/',
  plugins: [
    vue(),
    tailwindcss() // <-- On active le compilateur ici
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})