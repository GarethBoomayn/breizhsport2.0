<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

interface Product {
  id: number
  name: string
  description: string
  price: number
  stock: number
  category_id: number
  image_url: string | null
  category?: {
    id: number
    name: string
  }
}

const route = useRoute()
const router = useRouter()
const product = ref<Product | null>(null)
const loading = ref(true)
const error = ref('')
const quantity = ref(1)

// Récupérer les détails du produit
const fetchProduct = async () => {
  const productId = route.params.id
  if (!productId) {
    router.push('/')
    return
  }

  loading.value = true
  error.value = ''
  try {
    const response = await fetch(`http://localhost:8000/products/${productId}`)
    if (!response.ok) {
      throw new Error('Erreur lors de la récupération du produit')
    }
    product.value = await response.json()
    
    // Récupérer les détails de la catégorie
    if (product.value?.category_id) {
      const categoryResponse = await fetch(`http://localhost:8000/categories/${product.value.category_id}`)
      if (categoryResponse.ok) {
        const category = await categoryResponse.json()
        product.value.category = category
      }
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Une erreur est survenue'
    console.error(error.value)
  } finally {
    loading.value = false
  }
}

// Ajouter au panier
const addToCart = () => {
  if (!product.value) return
  
  // Récupérer le panier existant ou créer un nouveau
  const cart = JSON.parse(localStorage.getItem('cart') || '[]')
  
  // Vérifier si le produit est déjà dans le panier
  const existingProductIndex = cart.findIndex((item: any) => item.id === product.value?.id)
  
  if (existingProductIndex >= 0) {
    // Mettre à jour la quantité si le produit existe déjà
    cart[existingProductIndex].quantity += quantity.value
  } else {
    // Ajouter le produit au panier
    cart.push({
      id: product.value.id,
      name: product.value.name,
      price: product.value.price,
      image_url: product.value.image_url,
      quantity: quantity.value
    })
  }
  
  // Sauvegarder le panier dans le localStorage
  localStorage.setItem('cart', JSON.stringify(cart))
  
  // Réinitialiser la quantité
  quantity.value = 1
  
  // Afficher une notification (à implémenter)
  alert('Produit ajouté au panier')
}

// Incrémenter la quantité
const incrementQuantity = () => {
  if (product.value && quantity.value < product.value.stock) {
    quantity.value++
  }
}

// Décrémenter la quantité
const decrementQuantity = () => {
  if (quantity.value > 1) {
    quantity.value--
  }
}

onMounted(() => {
  fetchProduct()
})
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <button @click="router.back()" class="mb-6 flex items-center text-breizhblue-600 hover:text-breizhblue-800">
      <svg xmlns="http://www.w3.org/2000/svg" class="icon-md mr-1" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M9.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L7.414 9H15a1 1 0 110 2H7.414l2.293 2.293a1 1 0 010 1.414z" clip-rule="evenodd" />
      </svg>
      Retour
    </button>

    <div v-if="loading" class="text-center py-10">
      <p class="text-lg">Chargement du produit...</p>
    </div>

    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
      <strong class="font-bold">Erreur!</strong>
      <span class="block sm:inline">{{ error }}</span>
    </div>

    <div v-else-if="!product" class="text-center py-10">
      <p class="text-lg">Produit non trouvé</p>
      <router-link to="/" class="text-breizhblue-600 hover:underline mt-2 inline-block">Retour à l'accueil</router-link>
    </div>

    <div v-else class="bg-white rounded-lg shadow-lg overflow-hidden">
      <div class="md:flex">
        <div class="md:w-1/2 h-80 bg-gray-200 flex items-center justify-center">
          <img 
            v-if="product.image_url" 
            :src="product.image_url" 
            :alt="product.name" 
            class="h-full w-full object-cover"
          >
          <div v-else class="text-gray-400 text-center p-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon-md mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <p>Pas d'image</p>
          </div>
        </div>
        
        <div class="md:w-1/2 p-6">
          <div class="mb-2">
            <span v-if="product.category" class="bg-breizhblue-100 text-breizhblue-800 text-xs font-semibold px-2.5 py-0.5 rounded">
              {{ product.category.name }}
            </span>
          </div>
          
          <h1 class="text-2xl font-bold mb-2">{{ product.name }}</h1>
          
          <p class="text-3xl font-bold text-breizhblue-600 mb-4">{{ product.price.toFixed(2) }} €</p>
          
          <div class="mb-6">
            <h2 class="text-lg font-semibold mb-2">Description</h2>
            <p class="text-gray-700">{{ product.description }}</p>
          </div>
          
          <div class="mb-6">
            <p class="text-sm text-gray-600 mb-1">
              Disponibilité: 
              <span v-if="product.stock > 0" class="text-breizhblue-600 font-semibold">En stock ({{ product.stock }})</span>
              <span v-else class="text-red-600 font-semibold">Rupture de stock</span>
            </p>
          </div>
          
          <div v-if="product.stock > 0" class="mb-6">
            <label for="quantity" class="block text-sm font-medium text-gray-700 mb-2">Quantité</label>
            <div class="flex items-center">
              <button 
                @click="decrementQuantity" 
                class="bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-1 px-3 rounded-l"
              >
                -
              </button>
              <input 
                id="quantity" 
                type="number" 
                v-model="quantity" 
                min="1" 
                :max="product.stock" 
                class="w-16 text-center border-gray-300 focus:ring-breizhblue-500 focus:border-breizhblue-500 block"
              >
              <button 
                @click="incrementQuantity" 
                class="bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-1 px-3 rounded-r"
              >
                +
              </button>
            </div>
          </div>
          
          <button 
            @click="addToCart" 
            class="flex items-center justify-center px-6 py-3 bg-breizhblue-600 text-white rounded-lg hover:bg-breizhblue-700 transition duration-150 w-full md:w-auto"
            :disabled="product.stock <= 0"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="icon-md mr-1" viewBox="0 0 20 20" fill="currentColor">
              <path d="M3 1a1 1 0 000 2h1.22l.305 1.222a.997.997 0 00.01.042l1.358 5.43-.893.892C3.74 11.846 4.632 14 6.414 14H15a1 1 0 000-2H6.414l1-1H14a1 1 0 00.894-.553l3-6A1 1 0 0017 3H6.28l-.31-1.243A1 1 0 005 1H3zM16 16.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0zM6.5 18a1.5 1.5 0 100-3 1.5 1.5 0 000 3z" />
            </svg>
            <span v-if="product.stock > 0">Ajouter au panier</span>
            <span v-else>Indisponible</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
