<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

interface CartItem {
  id: number
  name: string
  price: number
  image_url: string | null
  quantity: number
}

const router = useRouter()
const cartItems = ref<CartItem[]>([])
const isCheckingOut = ref(false)

// Calculer le total du panier
const cartTotal = computed(() => {
  return cartItems.value.reduce((total, item) => total + (item.price * item.quantity), 0)
})

// Calculer le nombre total d'articles
const itemCount = computed(() => {
  return cartItems.value.reduce((count, item) => count + item.quantity, 0)
})

// Charger le panier depuis le localStorage
const loadCart = () => {
  const savedCart = localStorage.getItem('cart')
  if (savedCart) {
    cartItems.value = JSON.parse(savedCart)
  }
}

// Mettre à jour la quantité d'un article
const updateQuantity = (itemId: number, newQuantity: number) => {
  const itemIndex = cartItems.value.findIndex(item => item.id === itemId)
  if (itemIndex !== -1) {
    if (newQuantity <= 0) {
      removeItem(itemId)
    } else {
      cartItems.value[itemIndex].quantity = newQuantity
      saveCart()
    }
  }
}

// Supprimer un article du panier
const removeItem = (itemId: number) => {
  cartItems.value = cartItems.value.filter(item => item.id !== itemId)
  saveCart()
}

// Vider le panier
const clearCart = () => {
  cartItems.value = []
  saveCart()
}

// Sauvegarder le panier dans le localStorage
const saveCart = () => {
  localStorage.setItem('cart', JSON.stringify(cartItems.value))
}

// Passer à la caisse
const checkout = async () => {
  isCheckingOut.value = true
  
  // Simulation d'un processus de paiement
  setTimeout(() => {
    // Vider le panier après le paiement réussi
    clearCart()
    
    // Rediriger vers une page de confirmation
    router.push({ name: 'home', query: { checkout: 'success' } })
    
    isCheckingOut.value = false
  }, 2000)
}

onMounted(() => {
  loadCart()
})
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-8">Votre Panier</h1>
    
    <div v-if="cartItems.length === 0" class="bg-white rounded-lg shadow p-6 text-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
      </svg>
      <p class="text-lg mb-4">Votre panier est vide</p>
      <router-link to="/" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg inline-block">
        Continuer vos achats
      </router-link>
    </div>
    
    <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="md:col-span-2">
        <div class="bg-white rounded-lg shadow overflow-hidden">
          <div class="p-4 border-b">
            <h2 class="text-lg font-semibold">Articles ({{ itemCount }})</h2>
          </div>
          
          <div class="divide-y">
            <div v-for="item in cartItems" :key="item.id" class="p-4 flex flex-col sm:flex-row">
              <div class="sm:w-24 h-24 bg-gray-200 rounded flex items-center justify-center mb-4 sm:mb-0 sm:mr-4">
                <img 
                  v-if="item.image_url" 
                  :src="item.image_url" 
                  :alt="item.name" 
                  class="h-full w-full object-cover rounded"
                >
                <div v-else class="text-gray-400 text-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
              </div>
              
              <div class="flex-grow">
                <h3 class="text-lg font-semibold mb-1">{{ item.name }}</h3>
                <p class="text-blue-600 font-bold mb-2">{{ item.price.toFixed(2) }} €</p>
                
                <div class="flex items-center justify-between">
                  <div class="flex items-center">
                    <button 
                      @click="updateQuantity(item.id, item.quantity - 1)" 
                      class="bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-1 px-2 rounded-l"
                    >
                      -
                    </button>
                    <span class="w-10 text-center">{{ item.quantity }}</span>
                    <button 
                      @click="updateQuantity(item.id, item.quantity + 1)" 
                      class="bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-1 px-2 rounded-r"
                    >
                      +
                    </button>
                  </div>
                  
                  <button 
                    @click="removeItem(item.id)" 
                    class="text-red-600 hover:text-red-800"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="mt-4 flex justify-between">
          <router-link to="/" class="text-blue-600 hover:text-blue-800 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M9.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L7.414 9H15a1 1 0 110 2H7.414l2.293 2.293a1 1 0 010 1.414z" clip-rule="evenodd" />
            </svg>
            Continuer vos achats
          </router-link>
          
          <button 
            @click="clearCart" 
            class="text-red-600 hover:text-red-800"
          >
            Vider le panier
          </button>
        </div>
      </div>
      
      <div class="md:col-span-1">
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-semibold mb-4">Récapitulatif</h2>
          
          <div class="space-y-2 mb-4">
            <div class="flex justify-between">
              <span>Sous-total</span>
              <span>{{ cartTotal.toFixed(2) }} €</span>
            </div>
            <div class="flex justify-between">
              <span>Livraison</span>
              <span>Gratuite</span>
            </div>
          </div>
          
          <div class="border-t pt-4 mb-6">
            <div class="flex justify-between font-bold text-lg">
              <span>Total</span>
              <span>{{ cartTotal.toFixed(2) }} €</span>
            </div>
          </div>
          
          <button 
            @click="checkout" 
            class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="isCheckingOut"
          >
            <span v-if="isCheckingOut">Traitement en cours...</span>
            <span v-else>Passer à la caisse</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
