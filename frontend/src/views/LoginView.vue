<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const login = async () => {
  if (!email.value || !password.value) {
    error.value = 'Veuillez remplir tous les champs'
    return
  }

  loading.value = true
  error.value = ''

  try {
    // Utiliser l'URL absolue avec le port 80 pour passer par Nginx
    const response = await fetch('http://localhost/api/auth/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        username: email.value, // L'API utilise 'username' pour l'email
        password: password.value,
      }),
    })

    if (!response.ok) {
      let errorMessage = 'Échec de connexion';
      try {
        // Vérifier si la réponse contient du JSON valide
        const text = await response.text();
        if (text) {
          const errorData = JSON.parse(text);
          errorMessage = errorData.detail || errorMessage;
        }
      } catch (parseError) {
        console.error('Erreur lors du parsing de la réponse:', parseError);
      }
      throw new Error(errorMessage);
    }

    const data = await response.json()
    
    // Stocker le token dans le localStorage
    localStorage.setItem('auth_token', data.access_token)
    localStorage.setItem('user_info', JSON.stringify({
      email: email.value,
      is_admin: data.is_admin || false
    }))
    
    // Rediriger vers la page d'accueil
    router.push('/')
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Une erreur est survenue'
    console.error('Erreur de connexion:', err)
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
          Connexion à votre compte
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Ou
          <router-link to="/register" class="font-medium text-breizhblue-600 hover:text-breizhblue-500">
            créez un nouveau compte
          </router-link>
        </p>
      </div>
      
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
        <span class="block sm:inline">{{ error }}</span>
      </div>
      
      <form class="mt-8 space-y-6" @submit.prevent="login">
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
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-breizhblue-500 focus:border-breizhblue-500 focus:z-10 sm:text-sm" 
              placeholder="Adresse email" 
            />
          </div>
          <div>
            <label for="password" class="sr-only">Mot de passe</label>
            <input 
              id="password" 
              name="password" 
              type="password" 
              autocomplete="current-password" 
              required 
              v-model="password"
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-breizhblue-500 focus:border-breizhblue-500 focus:z-10 sm:text-sm" 
              placeholder="Mot de passe" 
            />
          </div>
        </div>

        <div>
          <button 
            type="submit" 
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-breizhblue-600 hover:bg-breizhblue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-breizhblue-500"
            :disabled="loading"
          >
            <span v-if="loading">Connexion en cours...</span>
            <span v-else>Se connecter</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
