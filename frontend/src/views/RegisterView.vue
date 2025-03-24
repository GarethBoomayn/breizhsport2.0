<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const username = ref('')
const fullName = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')
const loading = ref(false)

const register = async () => {
  // Validation des champs
  if (!email.value || !username.value || !fullName.value || !password.value || !confirmPassword.value) {
    error.value = 'Veuillez remplir tous les champs'
    return
  }

  if (password.value !== confirmPassword.value) {
    error.value = 'Les mots de passe ne correspondent pas'
    return
  }

  loading.value = true
  error.value = ''

  try {
    const response = await fetch('http://localhost:8000/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email.value,
        username: username.value,
        full_name: fullName.value,
        password: password.value
      }),
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Échec de l\'inscription')
    }

    // Rediriger vers la page de connexion avec un message de succès
    router.push({ 
      path: '/login', 
      query: { registered: 'success' } 
    })
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Une erreur est survenue'
    console.error('Erreur d\'inscription:', err)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Créer un compte
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Ou
          <router-link to="/login" class="font-medium text-blue-600 hover:text-blue-500">
            connectez-vous à votre compte existant
          </router-link>
        </p>
      </div>
      
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
        <span class="block sm:inline">{{ error }}</span>
      </div>
      
      <form class="mt-8 space-y-6" @submit.prevent="register">
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="email-address" class="sr-only">Adresse email</label>
            <input 
              id="email-address" 
              name="email" 
              type="email" 
              autocomplete="email" 
              required 
              v-model="email"
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" 
              placeholder="Adresse email" 
            />
          </div>
          <div>
            <label for="username" class="sr-only">Nom d'utilisateur</label>
            <input 
              id="username" 
              name="username" 
              type="text" 
              autocomplete="username" 
              required 
              v-model="username"
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" 
              placeholder="Nom d'utilisateur" 
            />
          </div>
          <div>
            <label for="full-name" class="sr-only">Nom complet</label>
            <input 
              id="full-name" 
              name="full_name" 
              type="text" 
              autocomplete="name" 
              required 
              v-model="fullName"
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" 
              placeholder="Nom complet" 
            />
          </div>
          <div>
            <label for="password" class="sr-only">Mot de passe</label>
            <input 
              id="password" 
              name="password" 
              type="password" 
              autocomplete="new-password" 
              required 
              v-model="password"
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" 
              placeholder="Mot de passe" 
            />
          </div>
          <div>
            <label for="confirm-password" class="sr-only">Confirmer le mot de passe</label>
            <input 
              id="confirm-password" 
              name="confirm_password" 
              type="password" 
              autocomplete="new-password" 
              required 
              v-model="confirmPassword"
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" 
              placeholder="Confirmer le mot de passe" 
            />
          </div>
        </div>

        <div>
          <button 
            type="submit" 
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            :disabled="loading"
          >
            <span v-if="loading">Inscription en cours...</span>
            <span v-else>S'inscrire</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
