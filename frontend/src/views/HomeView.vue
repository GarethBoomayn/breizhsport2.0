<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Product {
  id: number
  name: string
  description: string
  price: number
  stock: number
  category_id: number
  image_url: string | null
}

const products = ref<Product[]>([])
const categories = ref<any[]>([])
const loading = ref(true)
const error = ref('')
const selectedCategory = ref<number | null>(null)

// Fonction pour récupérer les produits
const fetchProducts = async (categoryId?: number) => {
  loading.value = true
  error.value = ''
  try {
    let url = 'http://localhost:8000/products'
    if (categoryId) {
      url += `?category_id=${categoryId}`
    }
    const response = await fetch(url)
    if (!response.ok) {
      throw new Error('Erreur lors de la récupération des produits')
    }
    products.value = await response.json()
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Une erreur est survenue'
    console.error(error.value)
  } finally {
    loading.value = false
  }
}

// Fonction pour récupérer les catégories
const fetchCategories = async () => {
  try {
    const response = await fetch('http://localhost:8000/categories')
    if (!response.ok) {
      throw new Error('Erreur lors de la récupération des catégories')
    }
    categories.value = await response.json()
  } catch (err) {
    console.error('Erreur lors de la récupération des catégories:', err)
  }
}

// Filtrer les produits par catégorie
const filterByCategory = (categoryId: number | null) => {
  selectedCategory.value = categoryId
  fetchProducts(categoryId || undefined)
}

onMounted(() => {
  fetchProducts()
  fetchCategories()
})
</script>

<template>
  <main class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-center mb-8">BreizhSport</h1>
    
    <!-- Filtres par catégorie -->
    <div class="mb-6">
      <h2 class="text-xl font-semibold mb-3">Catégories</h2>
      <div class="flex flex-wrap gap-2">
        <button 
          @click="filterByCategory(null)" 
          class="px-4 py-2 rounded-lg"
          :class="selectedCategory === null ? 'bg-breizhblue-600 text-white' : 'bg-gray-200 hover:bg-gray-300'"
        >
          Tous
        </button>
        <button 
          v-for="category in categories" 
          :key="category.id"
          @click="filterByCategory(category.id)"
          class="px-4 py-2 rounded-lg"
          :class="selectedCategory === category.id ? 'bg-breizhblue-600 text-white' : 'bg-gray-200 hover:bg-gray-300'"
        >
          {{ category.name }}
        </button>
      </div>
    </div>

    <!-- Affichage des produits -->
    <div v-if="loading" class="text-center py-10">
      <p class="text-lg">Chargement des produits...</p>
    </div>

    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
      <strong class="font-bold">Erreur!</strong>
      <span class="block sm:inline">{{ error }}</span>
    </div>

    <div v-else-if="products.length === 0" class="text-center py-10">
      <svg xmlns="http://www.w3.org/2000/svg" class="icon-lg mx-auto text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
      </svg>
      <p class="text-lg text-gray-600">Aucun produit trouvé</p>
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <div v-for="product in products" :key="product.id" class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
        <div class="h-48 bg-gray-200 flex items-center justify-center">
          <img 
            v-if="product.image_url" 
            :src="product.image_url" 
            :alt="product.name" 
            class="h-full w-full object-cover"
          >
          <div v-else class="text-gray-400 text-center p-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon-lg mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <p>Pas d'image</p>
          </div>
        </div>
        <div class="p-4">
          <h3 class="text-lg font-semibold mb-2 truncate">{{ product.name }}</h3>
          <p class="text-gray-600 text-sm mb-2 line-clamp-2">{{ product.description }}</p>
          <div class="flex justify-between items-center">
            <span class="text-breizhblue-600 font-bold">{{ product.price.toFixed(2) }} €</span>
            <router-link :to="`/product/${product.id}`" class="bg-breizhblue-600 hover:bg-breizhblue-700 text-white px-3 py-1 rounded-lg text-sm">
              Voir
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-clamp: 2;
}
</style>
