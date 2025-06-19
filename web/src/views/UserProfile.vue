<template>
  <div class="flex flex-col items-center px-6 pt-10 lg:pt-16 pb-24">
    <!-- Botão de Voltar -->
    <div class="absolute top-6 left-6">
      <button @click="goBack" class="flex items-center text-azul hover:text-laranja transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
        </svg>
        <span class="ml-2 font-medium">Voltar</span>
      </button>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="w-full h-64 flex flex-col items-center justify-center">
      <div class="w-12 h-12 rounded-full border-4 border-laranja border-t-transparent animate-spin"></div>
      <p class="mt-4 text-cinza3">Carregando perfil...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="w-full h-64 flex flex-col items-center justify-center text-center px-4">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-12 h-12 text-laranja">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
      </svg>
      <h2 class="text-lg font-bold text-azul mt-4">Erro ao carregar perfil</h2>
      <p class="mt-2 text-cinza3">{{ errorMessage }}</p>
      <button @click="fetchUserProfile" class="mt-4 bg-verde text-white px-6 py-2 rounded-full hover:scale-110 transition-transform">
        Tentar novamente
      </button>
    </div>

    <!-- User profile content -->
    <div v-else class="w-full flex flex-col items-center">
      <!-- Avatar -->
      <div class="w-24 h-24 lg:w-32 lg:h-32 rounded-full flex items-center justify-center border-4 border-laranja overflow-hidden">
        <img
          v-if="user.foto"
          :src="user.foto"
          alt="Foto do Usuário"
          class="w-full h-full object-cover"
        />
        <div
          v-else
          class="w-full h-full bg-cinza2 flex items-center justify-center text-cinza3 text-sm lg:text-lg"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="white"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="#FFFFFF"
            class="w-10 h-10"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z"
            />
          </svg>
        </div>
      </div>

      <!-- User info -->
      <h1 class="text-xl lg:text-3xl font-bold text-azul mt-4 lg:mt-6">
        {{
          user.first_name && user.last_name ? `${user.first_name} ${user.last_name}` : 
          user.first_name ? user.first_name : 
          user.last_name ? user.last_name : 
          user.username
        }}
      </h1>
      <p class="text-sm lg:text-lg text-cinza3" v-if="user.email">
        {{ user.email }}
      </p>
      <p class="text-sm lg:text-lg text-cinza3" v-else>
        {{ isOwnProfile ? "Email não disponível" : "Email protegido" }}
      </p>

      <p v-if="user.matricula" class="text-sm lg:text-lg text-cinza3">
        {{ isStudent ? 'Matrícula: ' : 'Identificação: ' }}{{ user.matricula }}
      </p>

      <!-- Status Badge -->
      <div class="mt-4 inline-flex items-center px-4 py-1 rounded-full" 
          :class="{'bg-verde/20 text-verde': user.is_active, 'bg-gray-200 text-gray-500': !user.is_active}">
        <span class="w-2 h-2 rounded-full mr-2" 
          :class="{'bg-verde': user.is_active, 'bg-gray-500': !user.is_active}"></span>
        <span class="text-sm font-medium">{{ user.is_active ? 'Ativo' : 'Inativo' }}</span>
      </div>

      <!-- Statistics -->
      <div class="w-full max-w-md mt-8 grid grid-cols-2 gap-4">
        <div class="bg-white rounded-xl p-4 shadow-complete flex flex-col items-center justify-center">
          <div class="text-azul text-2xl font-bold">{{ userStats.itemsFound || 0 }}</div>
          <div class="text-cinza3 text-sm">Itens achados</div>
        </div>
        <div class="bg-white rounded-xl p-4 shadow-complete flex flex-col items-center justify-center">
          <div class="text-azul text-2xl font-bold">{{ userStats.itemsLost || 0 }}</div>
          <div class="text-cinza3 text-sm">Itens perdidos</div>
        </div>
      </div>

      <!-- Security Action -->
      <div class="w-full max-w-md mt-8 bg-white rounded-xl p-6 shadow-complete">
        <h2 class="text-lg font-bold text-azul mb-4">Ação de Segurança</h2>
        
        <button v-if="reportingEnabled" @click="openReportDialog" 
          class="bg-red-600 text-white w-full font-medium py-4 rounded-full hover:scale-110 transition-transform duration-300 text-center text-lg lg:text-xl">
          Reportar Usuário
        </button>
      </div>

      <!-- Recent Items -->
      <div v-if="recentItems.length > 0" class="w-full max-w-md mt-8">
        <h2 class="text-lg font-bold text-azul mb-4">Itens Recentes</h2>
        
        <div class="space-y-4">
          <div v-for="item in recentItems" :key="item.id" 
            class="bg-white rounded-xl p-4 shadow-complete flex items-center space-x-4 cursor-pointer hover:bg-gray-50 transition-colors"
            @click="viewItem(item.id)">
            
            <div class="w-16 h-16 rounded-lg bg-cinza1 overflow-hidden flex-shrink-0">
              <img v-if="item.image" :src="item.image" alt="Item" class="w-full h-full object-cover" />
              <div v-else class="w-full h-full flex items-center justify-center text-cinza3">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" 
                  stroke="currentColor" class="w-6 h-6">
                  <path stroke-linecap="round" stroke-linejoin="round" 
                    d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
                </svg>
              </div>
            </div>
            
            <div class="flex-1 min-w-0">
              <h3 class="text-sm font-semibold text-azul truncate">{{ item.title }}</h3>
              <p class="text-xs text-cinza3 mt-1">{{ item.status }}</p>
              <p class="text-xs text-cinza3 mt-1">{{ formatDate(item.created_at) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer spacing for bottom menu -->
    <div class="h-16 lg:h-24"></div>
  </div>

  <!-- Report User Modal -->
  <div v-if="showReportModal" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
    <div class="bg-white rounded-lg w-full max-w-md p-6 shadow-lg">
      <h3 class="text-xl font-bold mb-4 text-gray-800">Denunciar usuário</h3>
      
      <p class="text-sm text-gray-600 mb-4">
        Informe o motivo da sua denúncia. Nossa equipe irá analisar e tomar as medidas necessárias.
      </p>
      
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-1">Categoria</label>
        <select 
          v-model="reportForm.category" 
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-laranja"
        >
          <option value="" disabled>Selecione um motivo</option>
          <optgroup label="Comportamento do Usuário">
            <option value="Ofensa/Abuso">Ofensa/Abuso</option>
            <option value="Assédio">Assédio</option>
            <option value="Comportamento suspeito">Comportamento suspeito</option>
            <option value="Mensagens inadequadas">Mensagens inadequadas</option>
          </optgroup>
          <optgroup label="Conteúdo">
            <option value="Perfil inapropriado">Perfil inapropriado</option>
            <option value="Imagem inadequada">Imagem inadequada</option>
            <option value="Informações falsas">Informações falsas</option>
          </optgroup>
          <optgroup label="Fraude">
            <option value="Golpe">Golpe</option>
            <option value="Spam">Spam</option>
            <option value="Item falso">Item falso</option>
            <option value="Item ilegal/proibido">Item ilegal/proibido</option>
          </optgroup>
          <optgroup label="Outros">
            <option value="Roubo de identidade">Roubo de identidade</option>
            <option value="Uso indevido da plataforma">Uso indevido da plataforma</option>
            <option value="Outros">Outros</option>
          </optgroup>
        </select>
      </div>
      
      <div class="mb-5">
        <label class="block text-sm font-medium text-gray-700 mb-1">Descrição</label>
        <textarea 
          v-model="reportForm.description" 
          rows="4" 
          placeholder="Descreva o problema com mais detalhes"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-laranja"
        ></textarea>
      </div>

      <div class="mb-5">
        <label class="block text-sm font-medium text-gray-700 mb-1">Anexo</label>
        <input 
          type="file" 
          @change="handleFileUpload" 
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-laranja"
        />
      </div>
      
      <div class="flex justify-end gap-3">
        <button 
          @click="closeReportDialog" 
          class="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300 transition-colors"
        >
          Cancelar
        </button>
        <button 
          @click="submitReport" 
          :disabled="isReportSubmitting"
          class="px-4 py-2 text-white bg-laranja rounded-md hover:bg-laranja/80 transition-colors disabled:bg-gray-400"
        >
          {{ isReportSubmitting ? 'Enviando...' : 'Enviar denúncia' }}
        </button>
      </div>
    </div>
  </div>

  <!-- Fixed Menu at Bottom -->
  <div class="fixed bottom-0 w-full">
    <MainMenu activeIcon="user" />
  </div>

  <Alert v-if="submitError" type="error" :message="alertMessage" @closed="submitError = false" />
  <Alert v-if="submitSuccess" type="success" :message="alertMessage" @closed="submitSuccess = false" />
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../services/api';
import MainMenu from '../components/Main-Menu.vue';
import Alert from '../components/Alert.vue';

const route = useRoute();
const router = useRouter();

// Estados principais
const user = ref({
  foto: '',
  first_name: '',
  last_name: '',
  email: '',
  username: '',
  matricula: null,
  is_active: true,
  isStudent: false,
  id: null
});

const currentUser = ref(null);

const userStats = ref({
  itemsLost: 0,
  itemsFound: 0
});

const recentItems = ref([]);
const loading = ref(true);
const error = ref(false);
const errorMessage = ref('');

// Estados para notificações
const submitError = ref(false);
const submitSuccess = ref(false);
const alertMessage = ref('');

// Estados para o modal de denúncia
const showReportModal = ref(false);
const reportForm = ref({
  category: '',
  description: '',
  file: null
});
const isReportSubmitting = ref(false);
const reportingEnabled = computed(() => user.value.id !== undefined);
const isStudent = computed(() => {
  const matricula = user.value.matricula;
  return matricula && /^\d{8,9}$/.test(matricula.toString());
});

const isOwnProfile = computed(() => {
  return currentUser.value?.id === user.value.id;
});

// Busca o usuário atual para comparar com o perfil exibido
async function fetchCurrentUser() {
  try {
    const response = await api.get('/auth/user/');
    currentUser.value = response.data;
  } catch (error) {
    console.error('Erro ao buscar usuário atual:', error);
  }
}

// Buscar dados do perfil do usuário
async function fetchUserProfile() {
  const userId = route.params.id;
  if (!userId) {
    error.value = true;
    errorMessage.value = 'ID de usuário não fornecido';
    loading.value = false;
    return;
  }

  try {
    loading.value = true;
    error.value = false;

    // Buscar dados do usuário
    const response = await api.get(`/auth/user-profile/${userId}/`);
    const matricula = response.data.matricula || null;
    
    user.value = {
      id: response.data.id,
      foto: response.data.foto || null,
      first_name: response.data.first_name || '',
      last_name: response.data.last_name || '',
      email: response.data.email || '',
      username: response.data.username || '',
      matricula: matricula,
      is_active: response.data.is_active !== undefined ? response.data.is_active : true
    };

    await fetchUserStats(userId);

    await fetchRecentItems(userId);

    loading.value = false;
  } catch (err) {
    console.error('Erro ao carregar perfil do usuário:', err);
    error.value = true;
    errorMessage.value = 'Não foi possível carregar os dados do usuário. Por favor, tente novamente mais tarde.';
    loading.value = false;
  }
}

async function fetchUserStats(userId) {
  try {
    const response = await api.get(`/auth/user-stats/${userId}/`);
    userStats.value = {
      itemsLost: response.data.items_lost || 0,
      itemsFound: response.data.items_found || 0
    };
  } catch (err) {
    console.error('Erro ao carregar estatísticas do usuário:', err);
    userStats.value = {
      itemsLost: 0,
      itemsFound: 0
    };
  }
}

async function fetchRecentItems(userId) {
  try {
    const response = await api.get(`/items/user/${userId}/recent/`);
    recentItems.value = response.data.map(item => ({
      id: item.id,
      title: item.title || item.name || 'Item sem nome',
      status: getStatusText(item.status),
      image: item.image || null,
      created_at: item.created_at
    })).slice(0, 3); 
  } catch (err) {
    console.error('Erro ao carregar itens recentes:', err);
    recentItems.value = [];
  }
}

function formatDate(dateString) {
  if (!dateString) return 'Data desconhecida';
  
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  }).format(date);
}

function getStatusText(status) {
  const statusMap = {
    'active': 'Ativo',
    'found': 'Encontrado',
    'lost': 'Perdido',
    'returned': 'Devolvido',
    'closed': 'Encerrado'
  };
  
  return statusMap[status] || status;
}

function goBack() {
  router.go(-1);
}


function viewItem(itemId) {
  if (!itemId) return;
  
  router.push({
    name: 'ListItem',
    query: { idItem: itemId }
  });
}

function openReportDialog() {
  showReportModal.value = true;
}

function closeReportDialog() {
  showReportModal.value = false;
  reportForm.value = {
    category: '',
    description: '',
    file: null
  };
}

function handleFileUpload(event) {
  reportForm.value.file = event.target.files[0] || null;
}

async function submitReport() {
  if (!reportForm.value.category) {
    alertMessage.value = 'Por favor, selecione uma categoria para a denúncia.';
    submitError.value = true;
    return;
  }

  if (!user.value.id) {
    alertMessage.value = 'Não foi possível identificar o usuário para denúncia.';
    submitError.value = true;
    return;
  }

  try {
    isReportSubmitting.value = true;

    const formData = new FormData();
    formData.append('reported_user', user.value.id);
    formData.append('categories', reportForm.value.category);
    formData.append('description', reportForm.value.description || '');
    formData.append('report_type', 'user'); 
    
    if (reportForm.value.file) {
      formData.append('attachment', reportForm.value.file);
    }

    await api.post('/reports/user/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    alertMessage.value = 'Denúncia enviada com sucesso!';
    submitSuccess.value = true;
    closeReportDialog();
  } catch (error) {
    console.error('Erro ao enviar denúncia:', error);
    alertMessage.value = 'Erro ao enviar denúncia. Só é possível enviar uma denúncia por usuário.';
    submitError.value = true;
  } finally {
    isReportSubmitting.value = false;
  }
}

onMounted(async () => {
  await fetchCurrentUser();
  await fetchUserProfile();
});
</script>

<style scoped>
</style>
