<template>
  <div
    class="fixed top-0 left-0 w-full bg-verde shadow-md py-3 px-4 flex items-center justify-between z-20"
    :class="{ visible: isVisible, invisible: !isVisible }"
  >
    <div class="flex items-center">
      <!-- Botão de Voltar -->
      <img
        @click="goBack"
        :src="LeftArrow"
        alt="Voltar"
        class="w-[35px] h-35[px] md:w-8 md:h-8 cursor-pointer transform transition duration-300 hover:scale-125"
      />

      <div class="flex items-center space-x-4 ml-2">
        <img
          @click="goToUserProfile"
          :src="userImage"
          alt="Foto do usuário"
          class="w-10 h-10 md:w-12 md:h-12 rounded-full object-cover border-2 border-white cursor-pointer hover:scale-105 transition-transform"
        />

        <!-- Nome do Usuário -->
        <span
          @click="goToUserProfile"
          class="text-white font-semibold text-sm md:text-base truncate max-w-[120px] md:max-w-[200px] cursor-pointer hover:underline"
        >
          {{ userName || "Usuário" }}
        </span>
      </div>
    </div>

    <!-- Centro: Logo -->
    <div class="hidden md:block absolute left-1/2 transform -translate-x-1/2">
      <router-link to="/about" class="no-underline text-white">
        <Logo class="pr-4" sizeClass="text-2xl" />
      </router-link>
    </div>
    
    <!-- Lado direito: Menu hambúrguer -->
    <div class="flex items-center justify-center">
      <div class="relative" ref="menuRef">
        <button 
          @click="showMenu = !showMenu" 
          class="p-2 rounded-full hover:bg-white/20 focus:outline-none focus:ring-2 focus:ring-white transition-all duration-300 transform active:scale-95"
          :class="{'bg-white/20': showMenu}"
          title="Menu de opções"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 text-white transition-transform duration-300" :class="{'rotate-90': showMenu}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        
        <div 
          v-if="showMenu" 
          class="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-lg border-2 border-gray-100 z-50 overflow-hidden"
        >
          <button 
            @click="openReportUserModal" 
            class="w-full text-left px-4 py-3 hover:bg-gray-100 text-red-600 flex items-center gap-3 transition-colors duration-200 border-b border-gray-100"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <span class="font-medium">Denunciar usuário</span>
          </button>
          
          <button 
            @click="goToItem" 
            class="w-full text-left px-4 py-3 hover:bg-gray-100 flex items-center gap-3 transition-colors duration-200 border-b border-gray-100 text-azul"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
            </svg>
            <span class="font-medium">Ver item</span>
          </button>
          
          <button 
            @click="goToUserProfile" 
            class="w-full text-left px-4 py-3 hover:bg-gray-100 flex items-center gap-3 transition-colors duration-200 text-azul"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            <span class="font-medium">Ver perfil do usuário</span>
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal de denúncia de usuário -->
  <div v-if="showReportUserModal" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
    <div class="bg-white rounded-lg w-full max-w-md p-6 shadow-lg">
      <h3 class="text-xl font-bold mb-4 text-gray-800">Denunciar usuário</h3>
      
      <p class="text-sm text-gray-600 mb-4">
        Informe o motivo da sua denúncia. Nossa equipe irá analisar e tomar as medidas necessárias.
      </p>
      
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-1">Categoria</label>
        <select 
          v-model="reportUserForm.category" 
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-laranja"
        >
          <option value="" disabled>Selecione um motivo</option>
          <option value="Ofensa/Abuso">Ofensa/Abuso</option>
          <option value="Spam">Spam</option>
          <option value="Assédio">Assédio</option>
          <option value="Golpe">Golpe</option>
          <option value="Mensagem inapropriada">Mensagem inapropriada</option>
          <option value="Outros">Outros</option>
        </select>
      </div>
      
      <div class="mb-5">
        <label class="block text-sm font-medium text-gray-700 mb-1">Descrição</label>
        <textarea 
          v-model="reportUserForm.description" 
          rows="4" 
          placeholder="Descreva o problema com mais detalhes"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-laranja"
        ></textarea>
      </div>

      <div class="mb-5">
        <label class="block text-sm font-medium text-gray-700 mb-1">Anexo</label>
        <input 
          type="file" 
          @change="handleUserFileUpload" 
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-laranja"
        />
      </div>
      
      <div class="flex justify-end gap-3">
        <button 
          @click="closeReportUserModal" 
          class="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300 transition-colors"
        >
          Cancelar
        </button>
        <button 
          @click="submitUserReport" 
          :disabled="isUserReportSubmitting"
          class="px-4 py-2 text-white bg-laranja rounded-md hover:bg-laranja/80 transition-colors disabled:bg-gray-400"
        >
          {{ isUserReportSubmitting ? 'Enviando...' : 'Enviar denúncia' }}
        </button>
      </div>
    </div>
  </div>

  <Alert v-if="submitError" type="error" :message="alertMessage" @closed="submitError = false" />
  <Alert v-if="submitSuccess" type="success" :message="alertMessage" @closed="submitSuccess = false" />
</template>

<script setup>
import { ref, onMounted, onUnmounted, watchEffect } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../services/api";
import Logo from "./Logo.vue";
import defaultAvatar from "@/assets/images/default-avatar.png";
import notAvailableImage from "@/assets/images/not-available.png";
import LeftArrow from "@/assets/icons/arrow-left-white.svg";
import Alert from "@/components/Alert.vue";

const route = useRoute();
const router = useRouter();
const chatroomId = ref(route.params.chatroomId || route.query.chatroomId);
const userName = ref("Usuário");
const userImage = ref(defaultAvatar);
const itemImage = ref(notAvailableImage);
const userId = ref(null);
const itemId = ref(null);
const currentUser = ref(null);

const fetchCurrentUser = async () => {
  try {
    const response = await api.get(`/auth/user/`);
    currentUser.value = response.data;
  } catch {}
};

const fetchChatroomData = async () => {
  if (!chatroomId.value || !currentUser.value?.id) return;

  try {
    const response = await api.get(`/chat/chatrooms/${chatroomId.value}/`);
    const chatroom = response.data;

    userId.value =
      chatroom.participant_1 === currentUser.value.id
        ? chatroom.participant_2
        : chatroom.participant_1;

    itemId.value = chatroom.item_id;

    fetchUserData();
    fetchItemData();
  } catch {}
};
const isVisible = ref(false);

// Variáveis para o menu e modal
const showMenu = ref(false);
const showReportUserModal = ref(false);
const isUserReportSubmitting = ref(false);
const reportUserForm = ref({
  category: "",
  description: "",
  attachment: null,
});
const alertMessage = ref("");
const submitError = ref(false);
const submitSuccess = ref(false);
const menuRef = ref(null);

const fetchUserData = async () => {
  if (!userId.value) return;
  try {
    const response = await api.get(`/auth/user-profile/${userId.value}/`);
    userName.value = response.data.first_name && response.data.last_name 
      ? `${response.data.first_name} ${response.data.last_name}`.trim() 
      : response.data.first_name 
        ? response.data.first_name 
        : response.data.last_name 
          ? response.data.last_name 
          : response.data.username || "Usuário";
    userImage.value = response.data.foto || defaultAvatar;
  } catch {}
};

const fetchItemData = async () => {
  if (!itemId.value) return;
  try {
    const response = await api.get(`/items/${itemId.value}`);
    itemImage.value = response.data.image_urls?.[0] || notAvailableImage;
  } catch {}
};

const goBack = () => {
  router.back();
};

// Funções para gerenciar o menu hambúrguer e modal de denúncia
const handleUserFileUpload = (event) => {
  const file = event.target.files[0];
  reportUserForm.value.attachment = file;
};

const openReportUserModal = () => {
  showReportUserModal.value = true;
  showMenu.value = false;
  reportUserForm.value = {
    category: "",
    description: "",
    attachment: null,
  };
};

const closeReportUserModal = () => {
  showReportUserModal.value = false;
};

const submitUserReport = async () => {
  if (!reportUserForm.value.category) {
    alertMessage.value = "Por favor, selecione uma categoria para a denúncia.";
    submitError.value = true;
    return;
  }

  const formData = new FormData();
  formData.append("report_type", "chat");
  formData.append("categories", reportUserForm.value.category);
  formData.append("description", reportUserForm.value.description);
  formData.append("reported_user", userId.value);
  formData.append("chatRoom", chatroomId.value);
  if (reportUserForm.value.attachment) {
    formData.append("attachment", reportUserForm.value.attachment);
  }

  try {
    isUserReportSubmitting.value = true;

    const response = await api.post("/reports/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    alertMessage.value = "Denúncia enviada com sucesso!";
    submitSuccess.value = true;
    closeReportUserModal();
  } catch (error) {
    console.error("Erro ao enviar denúncia:", error);
    alertMessage.value = "Erro ao enviar denúncia. Só é possível enviar uma denúncia por usuário.";
    submitError.value = true;
  } finally {
    isUserReportSubmitting.value = false;
  }
};

const goToItem = () => {
  if (itemId.value) {
    router.push({ name: "ListItem", query: { idItem: itemId.value } });
  } else {
    alertMessage.value = "Não foi possível encontrar informações do item.";
    submitError.value = true;
  }
  showMenu.value = false;
};

const goToUserProfile = () => {
  if (userId.value) {
    router.push({ name: "UserProfile", params: { id: userId.value } });
  } else {
    alertMessage.value = "Não foi possível encontrar informações do usuário.";
    submitError.value = true;
  }
  showMenu.value = false;
};

function handleClickOutside(event) {
  if (showMenu.value && menuRef.value && !menuRef.value.contains(event.target)) {
    showMenu.value = false;
  }
}

watchEffect(() => {
  if (!currentUser.value) {
    fetchCurrentUser();
  } else {
    fetchChatroomData();
  }
});

onMounted(() => {
  fetchCurrentUser();
  document.addEventListener("mousedown", handleClickOutside);

  setTimeout(() => {
    isVisible.value = true;
  }, 1);
});

onUnmounted(() => {
  document.removeEventListener("mousedown", handleClickOutside);
});
</script>

<style>
.visible {
  opacity: 1;
  transform: translateY(0);

  transition:
    opacity 0.3s ease-in-out,
    transform 0.3s ease-in-out;
}

.invisible {
  opacity: 0;
  transform: translateY(-45px);
}
</style>
