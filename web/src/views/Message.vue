<template>
  <div class="relative flex flex-col h-screen bg-gray-100">

    <div class="flex absolute inset-0 justify-center items-center pointer-events-none z-0">
      <img
        src="@/assets/icons/Favicon.png"
        alt="Watermark"
        class="w-48 md:w-64 lg:w-80 opacity-20"
      />
    </div>

    <HeaderMessage
      v-if="receiverId && itemId"
      :itemId="String(itemId)" 
      :userId="String(receiverId)"
      class="fixed top-0 left-0 w-full z-20"
    />
    
    <!-- Menu hambúrguer -->
    <div class="fixed top-0 right-0 h-[72px] pr-5 flex items-center justify-center z-30">
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
          class="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-lg border-2 border-gray-100 z-40 overflow-hidden"
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

    <div ref="messagesContainer" class="relative flex-1 pt-32 pb-24 px-4 overflow-y-auto z-10">
      <div v-for="message in messages" :key="message.id" class="mb-2 flex">
        
        <div v-if="message.sender === currentUser?.id" class="flex w-full justify-end">
          <div class="bg-laranja text-white p-3 rounded-2xl max-w-[70%] break-words shadow-md">
            <p class="text-sm">{{ message.content }}</p>
            <span class="text-xs opacity-75 mt-1 block text-right">
              {{ formatTime(message.timestamp) }}
            </span>
          </div>
        </div>

        <div v-else class="flex w-full justify-start">
          <div class="bg-gray-300 text-gray-800 p-3 rounded-2xl max-w-[70%] break-words shadow-md">
            <p class="text-sm">{{ message.content }}</p>
            <span class="text-xs opacity-75 mt-1 block text-left">
              {{ formatTime(message.timestamp) }}
            </span>
          </div>
        </div>

      </div>
    </div>
    
    <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-4 z-20">
      <div class="flex">
        <input
          v-model="messageContent"
          @keyup.enter="sendMessage"
          type="text"
          maxlength="80"
          placeholder="Digite uma mensagem (máx. 80 caracteres)..."
          class="flex-1 border border-gray-300 rounded-full px-4 py-2 focus:outline-none focus:border-laranja"
        />
        <button
          @click="sendMessage"
          :disabled="!messageContent.trim()"
          class="ml-2 bg-laranja text-white px-4 py-2 rounded-full hover:bg-laranja-dark disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Enviar
        </button>
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
import { ref, onMounted, onUnmounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../services/api";
import HeaderMessage from "@/components/Header-Message.vue";
import Alert from "@/components/Alert.vue";
import { io } from "socket.io-client";

const route = useRoute();
const router = useRouter();
const messages = ref([]);
const messageContent = ref("");
const currentUser = ref(null);
const item = ref(null);
const receiverId = ref(null);
const alertMessage = ref("");
const submitError = ref(false);
const submitSuccess = ref(false);

// Variáveis para o menu e modal
const showMenu = ref(false);
const showReportUserModal = ref(false);
const isUserReportSubmitting = ref(false);
const reportUserForm = ref({
  category: "",
  description: "",
  attachment: null,
});

const chatroomId = ref(route.params.chatroomId || route.query.chatroomId);
const itemId = ref(route.params.itemId || route.query.itemId);

const socket = ref(null);

const connectWebSocket = () => {
  const WS_URL = import.meta.env.VITE_WS_URL;

  socket.value = io(WS_URL, {
    transports: ["websocket"],
    path: "/socket.io/", // caminho padrão do socket.io, seu nginx já está configurado para /socket.io/
    query: { chatroomId: chatroomId.value }
  });

  socket.value.on("connect", () => {
    console.log("Socket.IO conectado:", socket.value.id);
  });

  socket.value.on("receive_message", (data) => {
    console.log("Nova mensagem recebida via Socket.IO:", data);
    messages.value.push(data);
    scrollToBottom();
  });

  socket.value.on("disconnect", () => {
    console.warn("Socket.IO desconectado.");
  });

  socket.value.on("connect_error", (err) => {
    console.error("Erro ao conectar no Socket.IO:", err);
  });
};


if (!chatroomId.value) {
  console.error("ID do chat não encontrado na rota");
} else {
  console.log("chatroomId:", chatroomId.value);
}

// const sendMessage = async () => {
//   if (!chatroomId.value) {
//     console.error("ID do chat não encontrado, não é possível enviar mensagem");
//     return;
//   }
//   if (!messageContent.value.trim()) {
//     console.warn("Mensagem vazia, nada a enviar");
//     return;
//   }
  
//   try {
//     console.log("Enviando mensagem para room:", chatroomId.value, "Conteúdo:", messageContent.value);
//     // Chama a API para enviar a mensagem
//     await api.post("/chat/messages/", {
//       room: chatroomId.value,
//       content: messageContent.value
//     });
//     messageContent.value = "";
//     await fetchMessages();
//   } catch (error) {
//     console.error("Erro ao enviar mensagem:", error.response?.data || error.message);
//   }
// };

const sendMessage = async () => {
  if (!chatroomId.value) {
    console.error("ID do chat não encontrado, não é possível enviar mensagem");
    return;
  }
  if (!messageContent.value.trim()) {
    console.warn("Mensagem vazia, nada a enviar");
    return;
  }

  const conteudo = messageContent.value.trim();

  try {
    console.log("Enviando mensagem para room:", chatroomId.value, "Conteúdo:", conteudo);

    // Primeiro, salva no banco de dados via API REST
    const response = await api.post("/chat/messages/", {
      room: chatroomId.value,
      content: conteudo
    });

    const mensagemSalva = response.data;

    // Agora, envia a mensagem pelo Socket.IO
    if (socket.value && socket.value.connected) {
      socket.value.emit("send_message", mensagemSalva);
    } else {
      console.warn("Socket.IO não está conectado. Mensagem salva no banco, mas não enviada em tempo real.");
    }

    messageContent.value = "";
    await fetchMessages();

  } catch (error) {
    console.error("Erro ao enviar mensagem:", error.response?.data || error.message);
    alertMessage.value = "Erro ao enviar mensagem.";
    submitError.value = true;
  }
};


const fetchMessages = async () => {
  if (!chatroomId.value) return;
  try {
    const response = await api.get("/chat/messages/", {
      params: { room: chatroomId.value }
    });
    messages.value = response.data.results || response.data;
  } catch (error) {
    console.error("Erro ao buscar mensagens:", error);
  }
};

const fetchCurrentUser = async () => {
  try {
    const response = await api.get("/auth/user/");
    currentUser.value = response.data;
  } catch (error) {
    console.error("Erro ao buscar usuário:", error);
  }
};

const fetchItem = async () => {
  if (!itemId.value) return;
  try {
    const response = await api.get(`/items/${itemId.value}`);
    item.value = response.data;
  } catch (error) {
    console.error("Erro ao buscar item:", error);
  }
};

const fetchReceiverId = async () => {
  if (!itemId.value) return;
  try {
    const response = await api.get(`/items/${itemId.value}`);
    receiverId.value = response.data.user_id;
  } catch (error) {
    console.error("Erro ao buscar dono do item:", error);
  }
};

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString("pt-BR", {
    hour: "2-digit",
    minute: "2-digit"
  });
};

const fetchChatroomData = async () => {
  if (!chatroomId.value) return;
  try {
    await api.get(`/chat/chatrooms/${chatroomId.value}/`);
    // Se necessário, processar os dados do chatroom aqui.
  } catch (error) {
    console.error("Erro ao buscar dados do chatroom:", error);
  }
};
const messagesContainer = ref(null);


const scrollToBottom = () => {
  const container = messagesContainer.value;
  if (container) {
    container.scrollTop = container.scrollHeight;
  }
};



onMounted(async () => {
  await fetchCurrentUser();
  await fetchItem();
  await fetchReceiverId();
  await fetchChatroomData();
  await fetchMessages();
  connectWebSocket();
});

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
  formData.append("reported_user", receiverId.value);
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
  if (receiverId.value) {
    router.push({ name: "UserProfile", params: { id: receiverId.value } });
  } else {
    alertMessage.value = "Não foi possível encontrar informações do usuário.";
    submitError.value = true;
  }
  showMenu.value = false;
};

const menuRef = ref(null);

function handleClickOutside(event) {
  if (showMenu.value && menuRef.value && !menuRef.value.contains(event.target)) {
    showMenu.value = false;
  }
}

onMounted(() => {
  document.addEventListener("mousedown", handleClickOutside);
});
onUnmounted(() => {
  document.removeEventListener("mousedown", handleClickOutside);
});
</script>

<style scoped></style>