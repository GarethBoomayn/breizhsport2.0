<script setup lang="ts">
import { RouterView } from 'vue-router'
import TheHeader from './components/TheHeader.vue'
</script>

<template>
  <div class="min-h-screen flex flex-col bg-breizhblue-50">
    <TheHeader />
    <main class="flex-grow container mx-auto px-4 py-6">
      <RouterView />
    </main>
    <footer class="bg-breizhblue-700 text-white py-6">
      <div class="container mx-auto px-4">
        <div class="flex flex-col md:flex-row justify-between items-center">
          <div class="mb-4 md:mb-0">
            <div class="text-xl font-bold flex items-center">
              <span>BreizhSport</span>
            </div>
            <p class="text-breizhblue-200 text-sm mt-2">La référence bretonne des articles de sport</p>
          </div>
          <div class="flex space-x-6">
            <a href="#" class="text-white hover:text-breizhblue-200 transition duration-150">Mentions légales</a>
            <a href="#" class="text-white hover:text-breizhblue-200 transition duration-150">CGV</a>
            <a href="#" class="text-white hover:text-breizhblue-200 transition duration-150">Contact</a>
          </div>
        </div>
        <div class="mt-6 text-center text-sm text-breizhblue-200">
          2025 BreizhSport. Tous droits réservés.
        </div>
      </div>
    </footer>
  </div>
</template>

<style>
/* Styles globaux */
body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #333;
}

/* Réinitialisation des styles pour les entrées numériques */
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  appearance: none;
  margin: 0;
}
input[type="number"] {
  -moz-appearance: textfield;
}

/* Styles de transition pour une navigation fluide */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.3s ease;
}
.page-enter-from,
.page-leave-to {
  opacity: 0;
}
</style>
