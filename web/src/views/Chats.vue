<template>
  <div class="fixed w-full top-0 z-[1]">
    <ItemHeader :title="'Mensagens'" :canEditUser="false" />
  </div>

  <div v-if="loadingChats" class="pt-32 pb-24 space-y-4">
    <div v-for="n in 3" :key="n" class="flex items-center px-6">
      <div class="w-[90px] h-[90px] rounded-full bg-cinza2 animate-pulse"></div>
      <div class="flex-1 px-4 space-y-2">
        <div class="h-7 bg-cinza2 rounded-md animate-pulse"></div>
        <div class="h-5 bg-cinza2 rounded-md animate-pulse"></div>
      </div>
    </div>
  </div>

  <div v-else-if="sortedChatrooms.length" class="pt-32 pb-24">
    <div
      v-for="chatroom in sortedChatrooms"
      :key="chatroom.id"
      class="flex items-center px-6 py-5 cursor-pointer transition-all duration-200 hover:bg-gray-200"
    >
      <img
        :src="chatroom.recipient.foto"
        alt="Foto do usuário"
        class="w-16 h-16 md:w-20 md:h-20 rounded-full object-cover border-2 border-white"
        @click.stop="openUserProfile(chatroom.recipient.id)"
      />

      <div class="ml-5 flex-1" @click="openChat(chatroom)">
        <div class="flex items-center justify-between">
          <p class="text-xl font-semibold text-gray-800">{{ chatroom.recipient.name }}</p>
          <span v-if="chatroom.unread_count > 0" 
                class="bg-laranja text-white text-xs font-bold px-2 py-1 rounded-full">
            {{ chatroom.unread_count }}
          </span>
        </div>
        <p class="text-md text-gray-500">Sobre o item: {{ chatroom.item_name }}</p>
      </div>
    </div>
  </div>

  <div v-else class="flex flex-col items-center justify-center h-96 mt-10">
    <p class="text-lg text-cinza3">Nenhuma conversa encontrada.</p>
  </div>

  <div class="fixed bottom-0 w-full bg-white shadow-md">
    <MainMenu :activeIcon="'chat'" />
  </div>

  <Alert v-if="submitError" type="error" :message="alertMessage" @closed="submitError = false" />
</template>

<script setup>
import { onMounted, ref, computed, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";
import ItemHeader from "../components/Item-Header.vue";
import MainMenu from "../components/Main-Menu.vue";
import defaultAvatar from "@/assets/images/default-avatar.png";
import Alert from "@/components/Alert.vue";
import { io } from "socket.io-client";

const router = useRouter();
const currentUser = ref(null);
const chatrooms = ref([]);
const loadingChats = ref(true);
const alertMessage = ref("");
const submitError = ref(false);
const socket = ref(null);

const sortedChatrooms = computed(() => {
  return [...chatrooms.value].sort((a, b) => {
    const dateA = a.last_message_timestamp ? new Date(a.last_message_timestamp) : new Date(0);
    const dateB = b.last_message_timestamp ? new Date(b.last_message_timestamp) : new Date(0);
    return dateB - dateA;
  });
});

const openChat = (chatroom) => {
  if (!chatroom.id || !chatroom.recipient || !chatroom.item_id) return;
  router.push({
    path: `/chat/${chatroom.id}`,
    query: {
      userId: chatroom.recipient.id,
      itemId: chatroom.item_id,
    },
  });
};

const openUserProfile = (userId) => {
  if (!userId) {
    alertMessage.value = "Não foi possível encontrar informações do usuário.";
    submitError.value = true;
    return;
  }
  router.push({ name: "UserProfile", params: { id: userId } });
};

async function fetchCurrentUser() {
  try {
    const response = await api.get(`/auth/user/`);
    currentUser.value = response.data;
    await fetchUserChatrooms();
  } catch (error) {
    console.error("Erro ao buscar usuário:", error);
    alertMessage = "Erro ao buscar usuário.";
    submitError = true;
  }
}

async function fetchUserChatrooms() {
  if (!currentUser.value?.id) return;

  try {
    const response = await api.get(`/chat/chatrooms/`);
    let chatroomsTemp = [];

    for (const chatroom of response.data.results) {
      if (
        chatroom.participant_1 === currentUser.value.id ||
        chatroom.participant_2 === currentUser.value.id
      ) {
        let otherUserId, otherUserName, otherUserFoto;

        if (chatroom.participant_1 === currentUser.value.id) {
          otherUserId = chatroom.participant_2;
          otherUserName = chatroom.participant_2_username;
        } else {
          otherUserId = chatroom.participant_1;
          otherUserName = chatroom.participant_1_username;
        }

        const userResponse = await api.get(`/users/${otherUserId}/`);
        otherUserFoto = userResponse.data.foto ? userResponse.data.foto : defaultAvatar;
        
        let lastMessageTimestamp = chatroom.created_at;
        try {
          const messagesResponse = await api.get("/chat/messages/", {
            params: { room: chatroom.id, limit: 1 }
          });
          
          if (messagesResponse.data.results && messagesResponse.data.results.length > 0) {
            lastMessageTimestamp = messagesResponse.data.results[0].timestamp;
          }
        } catch (err) {
          console.error(`Erro ao buscar última mensagem do chatroom ${chatroom.id}:`, err);
        }

        chatroomsTemp.push({
          ...chatroom,
          recipient: {
            id: otherUserId,
            name: otherUserName,
            foto: otherUserFoto,
          },
          unread_count: chatroom.unread_count || 0,
          last_message_timestamp: lastMessageTimestamp
        });
      }
    }

    chatrooms.value = chatroomsTemp;
  } catch (error) {
    console.error("Erro ao buscar conversas:", error);
    alertMessage.value = "Erro ao buscar conversas.";
    submitError.value = true;
  } finally {
    loadingChats.value = false;
  }
}

const connectWebSocket = () => {
  const WS_URL = import.meta.env.VITE_WS_URL;
  
  socket.value = io(WS_URL, {
    transports: ["websocket"],
    path: "/socket.io/"
  });

  socket.value.on("connect", () => {
    console.log("Socket.IO conectado na lista de chats:", socket.value.id);
  });

  socket.value.on("receive_message", (data) => {
    console.log("Nova mensagem recebida na lista de chats:", data);
    updateChatroomWithNewMessage(data);
  });
  
  socket.value.on("chatlist_update", (data) => {
    console.log("Atualização da lista de chats:", data);
    if (data.last_message) {
      updateChatroomWithNewMessage(data.last_message);
    }
  });
  
  socket.value.on("message_status_updated", (data) => {
    console.log("Status de mensagem atualizado na lista de chats:", data);
    updateUnreadMessageCount(data.chat_id);
  });

  socket.value.on("disconnect", () => {
    console.warn("Socket.IO desconectado da lista de chats.");
  });

  socket.value.on("connect_error", (err) => {
    console.error("Erro ao conectar no Socket.IO da lista de chats:", err);
  });
};

const updateChatroomWithNewMessage = (message) => {
  if (!message || !message.room) return;
  
  const chatroomIndex = chatrooms.value.findIndex(chat => chat.id === message.room);
  
  if (chatroomIndex !== -1) {
    const updatedChatroom = { 
      ...chatrooms.value[chatroomIndex],
      last_message_timestamp: message.timestamp
    };
    
    if (message.sender !== currentUser.value?.id) {
      updatedChatroom.unread_count = (updatedChatroom.unread_count || 0) + 1;
    }
    
    const updatedChatrooms = [...chatrooms.value];
    updatedChatrooms[chatroomIndex] = updatedChatroom;
    chatrooms.value = updatedChatrooms;
  } else {
    fetchUserChatrooms();
  }
};

const updateUnreadMessageCount = async (chatroomId) => {
  if (!chatroomId) return;
  
  try {
    const response = await api.get(`/chat/chatrooms/${chatroomId}/`);
    const updatedChatroom = response.data;
    
    const chatroomIndex = chatrooms.value.findIndex(chat => chat.id === chatroomId);
    if (chatroomIndex !== -1) {
      const updatedChatrooms = [...chatrooms.value];
      updatedChatrooms[chatroomIndex] = {
        ...updatedChatrooms[chatroomIndex],
        unread_count: updatedChatroom.unread_count || 0
      };
      chatrooms.value = updatedChatrooms;
    }
  } catch (error) {
    console.error(`Erro ao atualizar contador de mensagens não lidas do chatroom ${chatroomId}:`, error);
  }
};

onMounted(() => {
  fetchCurrentUser();
  connectWebSocket();
});

onUnmounted(() => {
  if (socket.value) {
    socket.value.disconnect();
  }
});
</script>

<style scoped>
@keyframes pulse {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.4;
  }
  100% {
    opacity: 1;
  }
}

.animate-pulse {
  animation: pulse 1.5s infinite;
}
</style>
