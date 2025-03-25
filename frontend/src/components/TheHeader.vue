<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isLoggedIn = ref(false)
const userInfo = ref<{ email: string; is_admin: boolean } | null>(null)
const showMobileMenu = ref(false)
const cartItemCount = ref(0)

// Fonction pour basculer le menu mobile
const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

// Vérifier si l'utilisateur est connecté
const checkAuthStatus = () => {
  const token = localStorage.getItem('auth_token')
  isLoggedIn.value = !!token
  
  const userInfoStr = localStorage.getItem('user_info')
  
  if (userInfoStr) {
    try {
      userInfo.value = JSON.parse(userInfoStr)
    } catch (e) {
      userInfo.value = null
    }
  }
}

// Calculer le nombre d'articles dans le panier
const updateCartCount = () => {
  const cart = localStorage.getItem('cart')
  if (cart) {
    try {
      const cartItems = JSON.parse(cart)
      cartItemCount.value = cartItems.reduce((count: number, item: any) => count + item.quantity, 0)
    } catch (e) {
      cartItemCount.value = 0
    }
  } else {
    cartItemCount.value = 0
  }
}

// Se déconnecter
const logout = () => {
  localStorage.removeItem('auth_token')
  localStorage.removeItem('user_info')
  isLoggedIn.value = false
  router.push('/')
}

// Écouter les changements dans le panier
window.addEventListener('storage', (event) => {
  if (event.key === 'cart') {
    updateCartCount()
  }
})

onMounted(() => {
  checkAuthStatus()
  updateCartCount()
})
</script>

<template>
  <header class="bg-breizhblue-700 shadow-md">
    <div class="container mx-auto px-4">
      <div class="flex justify-between items-center py-3">
        <!-- Logo et navigation principale -->
        <div class="flex">
          <div class="flex-shrink-0 flex items-center">
            <router-link to="/" class="flex items-center">
              <img src="/logo-small.png" alt="BreizhSport Logo" class="h-5 w-5 mr-2 img-sm" />
              <span class="text-xl font-bold text-white hidden md:block">BreizhSport</span>
            </router-link>
          </div>
          <nav class="hidden md:ml-6 md:flex md:space-x-4 items-center">
            <router-link to="/" class="px-3 py-2 rounded-md text-sm font-medium text-white hover:bg-breizhblue-600 transition duration-150">Accueil</router-link>
            <router-link to="/about" class="px-3 py-2 rounded-md text-sm font-medium text-white hover:bg-breizhblue-600 transition duration-150">À propos</router-link>
          </nav>
        </div>
        
        <!-- Actions utilisateur -->
        <div class="hidden md:flex items-center space-x-4">
          <!-- Utilisateur non connecté -->
          <template v-if="!isLoggedIn">
            <router-link to="/login" class="text-sm font-medium text-white hover:text-breizhblue-200 transition duration-150">Connexion</router-link>
            <router-link to="/register" class="ml-4 px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-breizhblue-700 bg-white hover:bg-breizhblue-50 transition duration-150">
              Inscription
            </router-link>
          </template>
          
          <!-- Utilisateur connecté -->
          <div v-else class="ml-3 relative">
            <div>
              <button @click="toggleMobileMenu" class="flex text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-breizhblue-300">
                <span class="sr-only">Ouvrir le menu utilisateur</span>
                <div class="h-8 w-8 rounded-full bg-breizhblue-500 flex items-center justify-center text-white">
                  {{ userInfo?.email?.charAt(0).toUpperCase() || 'U' }}
                </div>
              </button>
            </div>
            
            <!-- Menu déroulant utilisateur -->
            <div v-if="showMobileMenu" class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 z-10">
              <div class="px-4 py-2 text-xs text-gray-500">
                Connecté en tant que <span class="font-medium">{{ userInfo?.email }}</span>
              </div>
              <router-link to="/profile" class="block px-4 py-2 text-sm text-gray-700 hover:bg-breizhblue-50">Profil</router-link>
              <button @click="logout" class="w-full text-left block px-4 py-2 text-sm text-gray-700 hover:bg-breizhblue-50">
                Déconnexion
              </button>
            </div>
          </div>
        </div>
        
        <!-- Menu mobile -->
        <div class="flex items-center ml-4 md:hidden">
          <router-link to="/cart" class="relative p-2 mr-2 rounded-full text-white hover:bg-breizhblue-600 transition duration-150">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon-md" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <span v-if="cartItemCount > 0" class="absolute top-0 right-0 inline-flex items-center justify-center px-1.5 py-0.5 text-xs font-bold leading-none text-white transform translate-x-1/2 -translate-y-1/2 bg-breizhblue-500 rounded-full">
              {{ cartItemCount }}
            </span>
          </router-link>
          
          <button @click="toggleMobileMenu" class="text-white hover:text-breizhblue-200 transition duration-150">
            <svg v-if="!showMobileMenu" xmlns="http://www.w3.org/2000/svg" class="icon-md" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="icon-md" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Menu mobile déroulant -->
    <div v-if="showMobileMenu" class="md:hidden bg-breizhblue-800">
      <div class="px-2 pt-2 pb-3 space-y-1">
        <router-link to="/" class="block px-3 py-2 rounded-md text-base font-medium text-white hover:bg-breizhblue-600 transition duration-150">Accueil</router-link>
        <router-link to="/about" class="block px-3 py-2 rounded-md text-base font-medium text-white hover:bg-breizhblue-600 transition duration-150">À propos</router-link>
      </div>
      <div class="pt-4 pb-3 border-t border-breizhblue-600">
        <div v-if="isLoggedIn" class="px-2 space-y-1">
          <div class="px-4 py-2 text-sm text-breizhblue-200">
            Connecté en tant que <span class="font-medium text-white">{{ userInfo?.email }}</span>
          </div>
          <router-link to="/profile" class="block px-3 py-2 rounded-md text-base font-medium text-white hover:bg-breizhblue-600 transition duration-150">Profil</router-link>
          <button @click="logout" class="w-full text-left block px-3 py-2 rounded-md text-base font-medium text-white hover:bg-breizhblue-600 transition duration-150">
            Déconnexion
          </button>
        </div>
        <div v-else class="px-2 space-y-1">
          <router-link to="/login" class="block px-3 py-2 rounded-md text-base font-medium text-white hover:bg-breizhblue-600 transition duration-150">Connexion</router-link>
          <router-link to="/register" class="block px-3 py-2 rounded-md text-base font-medium text-white hover:bg-breizhblue-600 transition duration-150">Inscription</router-link>
        </div>
      </div>
    </div>
  </header>
</template>
