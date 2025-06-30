<template>
  <div class="fixed w-full top-0 z-[1]">
    <UserHeader />
  </div>

  <div class="flex flex-col items-center px-6 pt-[80px] md:pt-[100px] pb-24">
    <div class="w-full max-w-2xl bg-white rounded-xl shadow-lg overflow-hidden">
      <div class="bg-white h-32 md:h-15 relative"></div>
      
      <div class="relative -mt-16 md:-mt-20 flex justify-center">
        <div class="w-32 h-32 md:w-40 md:h-40 rounded-full border-4 border-laranja bg-white flex items-center justify-center overflow-hidden shadow-lg">
          <img
            v-if="user.foto"
            :src="user.foto"
            alt="Foto do Usuário"
            class="w-full h-full object-cover"
          />
          <div
            v-else
            class="w-full h-full bg-cinza2 flex items-center justify-center text-cinza3"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="white"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="#FFFFFF"
              class="w-14 h-14 md:w-20 md:h-20"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z"
              />
            </svg>
          </div>
        </div>
      </div>

      <div class="px-6 py-4 text-center">
        <h2 class="text-2xl md:text-3xl font-bold text-azul">
          {{ 
            user.first_name && user.last_name ? user.first_name + " " + user.last_name : 
            user.first_name ? user.first_name : 
            user.last_name ? user.last_name : 
            user.username
          }}
        </h2>
        <p class="text-base md:text-lg text-gray-600 mt-2">
          {{ user.email || "Email não disponível" }}
        </p>
        <p v-if="user.matricula" class="text-base md:text-lg text-gray-600">
          Matrícula: {{ user.matricula }}
        </p>
        
        <div class="grid grid-cols-2 md:grid-cols-3 gap-4 mt-8 mb-6 text-center">
          <div class="bg-gray-50 p-4 rounded-lg shadow-sm">
            <p class="text-2xl md:text-3xl font-bold text-laranja">{{ stats.itemsFound }}</p>
            <p class="text-sm md:text-base text-gray-600">Itens achados</p>
          </div>
          <div class="bg-gray-50 p-4 rounded-lg shadow-sm">
            <p class="text-2xl md:text-3xl font-bold text-laranja">{{ stats.itemsLost }}</p>
            <p class="text-sm md:text-base text-gray-600">Itens perdidos</p>
          </div>
          <div class="bg-gray-50 p-4 rounded-lg shadow-sm col-span-2 md:col-span-1">
            <p class="text-2xl md:text-3xl font-bold text-laranja">{{ stats.chats }}</p>
            <p class="text-sm md:text-base text-gray-600">Conversas abertas</p>
          </div>
        </div>
      </div>
    </div>

    <div class="w-full max-w-2xl mt-8 space-y-4 md:space-y-6">
      <router-link to="/user-items-lost" class="w-full flex justify-center">
        <button
          class="bg-verde text-white w-full md:w-[80%] lg:w-[70%] font-medium py-4 md:py-5 lg:py-6 rounded-full hover:scale-105 transition-transform duration-300 text-center text-lg md:text-xl lg:text-2xl shadow-lg border-2 border-verde/20"
        >
          Meus itens ativos
        </button>
      </router-link>
      <div class="w-full flex justify-center">
        <button
          @click="openReportModal"
          class="bg-azul text-white w-full md:w-[80%] lg:w-[70%] font-medium py-4 md:py-5 lg:py-6 rounded-full hover:scale-105 transition-transform duration-300 text-center text-lg md:text-xl lg:text-2xl shadow-lg border-2 border-azul/20"
        >
          Reportar um problema
        </button>
      </div>
      <button
        @click="handleLogout"
        class="w-full flex justify-center"
      >
        <span class="bg-red-600 text-white w-full md:w-[80%] lg:w-[70%] font-medium py-4 md:py-5 lg:py-6 rounded-full hover:scale-105 transition-transform duration-300 text-center text-lg md:text-xl lg:text-2xl shadow-lg border-2 border-laranja/20 mb-6">
          Sair da Conta
        </span>
      </button>
    </div>

    <div class="fixed bottom-0 w-full">
      <MainMenu activeIcon="user" />
    </div>
  </div>

  <Alert v-if="submitError" type="error" :message="alertMessage" @closed="submitError = false" />
  <Alert v-if="submitSuccess" type="success" :message="alertMessage" @closed="submitSuccess = false" />
  
  <ReportProblemModal 
    :is-open="isReportModalOpen" 
    :user-email="user.email" 
    @close="closeReportModal" 
    @success="handleReportSuccess" 
    @error="handleReportError"
  />
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";
import MainMenu from "../components/Main-Menu.vue";
import Alert from "@/components/Alert.vue";
import { useRouter } from "vue-router";
import UserHeader from "@/components/Header-User.vue";
import ReportProblemModal from "@/components/ReportProblemModal.vue";

const user = ref({
  foto: "",
  first_name: "",
  last_name: "",
  email: "",
  username: "",
  matricula: null,
});
const stats = ref({
  itemsFound: 0,
  itemsLost: 0,
  chats: 0,
});
const alertMessage = ref("");
const submitError = ref(false);
const submitSuccess = ref(false);
const router = useRouter();
const isReportModalOpen = ref(false);

async function fetchUserData() {
  try {
    const response = await api.get("/auth/user/");
    user.value = {
      id: response.data.id,
      foto: response.data.foto || null,
      first_name: response.data.first_name,
      last_name: response.data.last_name,
      email: response.data.email,
      username: response.data.username,
      matricula: response.data.matricula,
    };

    // Chama a nova função para buscar estatísticas
    fetchUserStats();
  } catch (error) {
    console.error("Erro ao carregar dados do usuário:", error);
    alertMessage.value = "Erro ao carregar dados do usuário.";
    submitError.value = true;
  }
}

async function fetchUserStats() {
  try {
    const userId = user.value.id;
    
    if (userId) {
      const userStatsResponse = await api.get(`/auth/user-stats/${userId}/`);
      
      try {
        const chatResponse = await api.get(`/chat/chatrooms/`);
        let chatsSet = new Set(); // Usamos um conjunto para evitar duplicatas
        
        if (chatResponse.data) {
          let chatsList = [];
          
          if (Array.isArray(chatResponse.data)) {
            chatsList = chatResponse.data;
          } else if (chatResponse.data.results && Array.isArray(chatResponse.data.results)) {
            chatsList = chatResponse.data.results;
          }
          
          chatsList.forEach(chat => {
            if (chat.participant_1 === userId || chat.participant_2 === userId) {
              chatsSet.add(chat.id); // Adiciona o ID único do chat ao conjunto
            }
          });
        }
        
        console.log('Total de chats únicos:', chatsSet.size);
        
        const totalChats = chatsSet.size;
        
        stats.value = {
          itemsFound: userStatsResponse.data.items_found || 0,
          itemsLost: userStatsResponse.data.items_lost || 0,
          chats: totalChats
        };
      } catch (chatError) {
        console.error("Erro ao buscar chats do usuário:", chatError);
        
        stats.value = {
          itemsFound: userStatsResponse.data.items_found || 0,
          itemsLost: userStatsResponse.data.items_lost || 0,
          chats: 0
        };
      }
    } else {
      console.error("ID do usuário não disponível para buscar estatísticas");
    }
  } catch (error) {
    console.error("Erro ao carregar estatísticas do usuário:", error);
  }
}

async function handleLogout() {
  try {
    await api.post("/logout/");
  } catch (e) {
  }
  // Limpa todos os cookies (incluindo tokens)
  document.cookie.split(";").forEach((c) => {
    document.cookie = c
      .replace(/^ +/, "")
      .replace(/=.*/, "=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/");
  });
  router.replace({ name: "Login" });
}

function openReportModal() {
  isReportModalOpen.value = true;
}

function closeReportModal() {
  isReportModalOpen.value = false;
}

function handleReportSuccess(message) {
  alertMessage.value = message;
  submitSuccess.value = true;
}

function handleReportError(message) {
  alertMessage.value = message;
  submitError.value = true;
}

onMounted(fetchUserData);
</script>

<style scoped></style>
