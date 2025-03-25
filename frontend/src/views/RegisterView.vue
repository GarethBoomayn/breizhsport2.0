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
const debugInfo = ref('')

const register = async () => {
  // Validation des champs
  if (!email.value || !username.value || !password.value || !confirmPassword.value) {
    error.value = 'Veuillez remplir tous les champs obligatoires'
    return
  }

  if (!email.value.includes('@') || !email.value.includes('.')) {
    error.value = 'Veuillez entrer une adresse email valide'
    return
  }

  if (username.value.length < 3) {
    error.value = 'Le nom d\'utilisateur doit contenir au moins 3 caractères'
    return
  }

  if (password.value.length < 8) {
    error.value = 'Le mot de passe doit contenir au moins 8 caractères'
    return
  }

  if (password.value !== confirmPassword.value) {
    error.value = 'Les mots de passe ne correspondent pas'
    return
  }

  loading.value = true
  error.value = ''
  debugInfo.value = ''

  try {
    // Log pour le débogage
    console.log('Tentative d\'inscription avec:', { 
      email: email.value, 
      username: username.value, 
      full_name: fullName.value || undefined 
    });
    
    // Utiliser l'URL absolue avec le port 80 pour passer par Nginx
    const response = await fetch('http://localhost/api/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email.value,
        username: username.value,
        full_name: fullName.value || undefined, // Envoyer undefined si vide pour utiliser la valeur par défaut
        password: password.value
      }),
    })

    // Log pour le débogage
    console.log('Réponse reçue:', { 
      status: response.status, 
      statusText: response.statusText,
      headers: Object.fromEntries([...response.headers])
    });

    if (!response.ok) {
      let errorMessage = 'Échec de l\'inscription';
      try {
        // Vérifier si la réponse contient du JSON valide
        const text = await response.text();
        debugInfo.value = `Réponse brute: ${text}`;
        console.log('Réponse brute:', text);
        
        if (text) {
          try {
            const errorData = JSON.parse(text);
            console.log('Données d\'erreur parsées:', errorData);
            
            if (errorData.detail && Array.isArray(errorData.detail)) {
              // Format d'erreur FastAPI standard
              errorMessage = errorData.detail.map((err) => `${err.loc[1]}: ${err.msg}`).join(', ');
            } else if (errorData.detail) {
              errorMessage = errorData.detail;
              
              // Gérer les erreurs spécifiques
              if (errorData.detail === "Email already registered") {
                errorMessage = "Cette adresse email est déjà utilisée";
              }
            }
          } catch (jsonError) {
            console.error('Erreur lors du parsing JSON:', jsonError);
            errorMessage = `Erreur de format: ${text}`;
          }
        }
      } catch (parseError) {
        console.error('Erreur lors du parsing de la réponse:', parseError);
        debugInfo.value = `Erreur de parsing: ${parseError.message}`;
      }
      throw new Error(errorMessage);
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
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="register">
        <div class="rounded-md shadow-sm -space-y-px">
          <div class="mb-4">
            <label for="email" class="block text-sm font-medium text-gray-700">Adresse email</label>
            <input id="email" name="email" type="email" autocomplete="email" required 
              v-model="email"
              class="mt-1 appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" 
            />
          </div>
          
          <div class="mb-4">
            <label for="username" class="block text-sm font-medium text-gray-700">Nom d'utilisateur</label>
            <input id="username" name="username" type="text" autocomplete="username" required 
              v-model="username"
              class="mt-1 appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" 
            />
          </div>
          
          <div class="mb-4">
            <label for="fullName" class="block text-sm font-medium text-gray-700">Nom complet</label>
            <input id="fullName" name="fullName" type="text" autocomplete="name" 
              v-model="fullName"
              class="mt-1 appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" 
            />
          </div>
          
          <div class="mb-4">
            <label for="password" class="block text-sm font-medium text-gray-700">Mot de passe</label>
            <input id="password" name="password" type="password" autocomplete="new-password" required 
              v-model="password"
              class="mt-1 appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" 
            />
          </div>
          
          <div class="mb-4">
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700">Confirmer le mot de passe</label>
            <input id="confirmPassword" name="confirmPassword" type="password" autocomplete="new-password" required 
              v-model="confirmPassword"
              class="mt-1 appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" 
            />
          </div>
        </div>

        <div v-if="error" class="bg-red-50 border-l-4 border-red-400 p-4 mb-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-sm text-red-700">{{ error }}</p>
              <p v-if="debugInfo" class="text-xs text-gray-500 mt-1">{{ debugInfo }}</p>
            </div>
          </div>
        </div>

        <div>
          <button type="submit" 
            :disabled="loading"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <span v-if="loading" class="absolute left-0 inset-y-0 flex items-center pl-3">
              <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            S'inscrire
          </button>
        </div>
        
        <div class="text-sm text-center">
          <router-link to="/login" class="font-medium text-blue-600 hover:text-blue-500">
            Déjà inscrit ? Se connecter
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>
