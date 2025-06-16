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

    <div ref="messagesContainer" class="relative flex-1 pt-32 pb-24 px-4 overflow-y-auto z-10">
      <div v-for="message in messages" :key="message.id" class="mb-2 flex">
        
        <div v-if="message.sender === currentUser?.id" class="flex w-full justify-end">
          <div class="bg-laranja text-white p-3 rounded-2xl max-w-[70%] break-words shadow-md">
            <p class="text-sm">{{ message.content }}</p>
            <div class="flex items-center justify-end mt-1">
              <span v-if="message.is_read" class="text-xs mr-1 text-white">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="inline-block" viewBox="0 0 16 16">
                  <path d="M8.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L2.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093L8.95 4.992a.252.252 0 0 1 .02-.022zm-.92 5.14.92.92a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 1 0-1.091-1.028L9.477 9.417l-.485-.486-.943 1.179z"/>
                </svg>
              </span>
              <span v-else class="text-xs mr-1 text-white">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="inline-block" viewBox="0 0 16 16">
                  <path d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.267.267 0 0 1 .02-.022z"/>
                </svg>
              </span>
              <span class="text-xs opacity-75">
                {{ formatTime(message.timestamp) }}
              </span>
            </div>
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
      <div class="relative">
        <div v-if="showEmojiPicker" class="absolute bottom-full mb-2 bg-white p-2 rounded-lg shadow-lg border border-gray-300 z-30 max-h-64 overflow-y-auto">
          <div class="grid grid-cols-8 gap-1">
            <button 
              v-for="emoji in emojis" 
              :key="emoji" 
              @click="addEmoji(emoji)" 
              class="text-xl p-1 hover:bg-gray-100 rounded transition-colors"
            >
              {{ emoji }}
            </button>
          </div>
        </div>
        
        <div class="flex items-center">
          <button
            @click="toggleEmojiPicker"
            class="p-2 text-gray-500 hover:text-laranja focus:outline-none mr-2"
            title="Inserir emoji"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.182 15.182a4.5 4.5 0 01-6.364 0M21 12a9 9 0 11-18 0 9 9 0 0118 0zM9.75 9.75c0 .414-.168.75-.375.75S9 10.164 9 9.75 9.168 9 9.375 9s.375.336.375.75zm-.375 0h.008v.015h-.008V9.75zm5.625 0c0 .414-.168.75-.375.75s-.375-.336-.375-.75.168-.75.375-.75.375.336.375.75zm-.375 0h.008v.015h-.008V9.75z" />
            </svg>
          </button>
          
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
    
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../services/api";
import HeaderMessage from "@/components/Header-Message.vue";
import { io } from "socket.io-client";

const route = useRoute();
const router = useRouter();
const messages = ref([]);
const messageContent = ref("");
const currentUser = ref(null);
const item = ref(null);
const receiverId = ref(null);
const showEmojiPicker = ref(false);

const emojis = [
  "😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😊", "😇", 
  "🙂", "🙃", "😉", "😌", "😍", "🥰", "😘", "😗", "😙", "😚", 
  "😋", "😛", "😝", "😜", "🤪", "🤨", "🧐", "🤓", "😎", "🤩", 
  "😏", "😒", "😞", "😔", "😟", "😕", "🙁", "☹️", "😣", "😖", 
  "😫", "😩", "🥺", "😢", "😭", "😤", "😠", "😡", "🤬", "🤯", 
  "❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎", "💔", 
  "👍", "👎", "👏", "🙌", "🤝", "🙏", "✌️", "🤞", "🤟", "🤘"
];

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
    if (chatroomId.value) {
      socket.value.emit('join_chat', chatroomId.value);
    }
  });

  socket.value.on("receive_message", (data) => {
    console.log("Nova mensagem recebida via Socket.IO:", data);
    messages.value.push(data);
    scrollToBottom();
    
    if (data.sender !== currentUser.value?.id) {
      markMessageAsRead(data.id);
    }
  });
  
  socket.value.on("message_status_updated", (data) => {
    console.log("Status de mensagem atualizado:", data);
    if (data.chat_id === chatroomId.value) {
      updateMessagesReadStatus(data.message_ids);
    }
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
  }
};


const fetchMessages = async () => {
  if (!chatroomId.value) return;
  try {
    const response = await api.get("/chat/messages/", {
      params: { room: chatroomId.value }
    });
    messages.value = response.data.results || response.data;
    
    markMessagesAsRead();
    
    setTimeout(() => {
      scrollToBottom();
    }, 100);
  } catch (error) {
    console.error("Erro ao buscar mensagens:", error);
  }
};

const markMessagesAsRead = async () => {
  if (!chatroomId.value || !currentUser.value?.id) return;
  
  try {
    const unreadMessages = messages.value.filter(
      msg => !msg.is_read && msg.sender !== currentUser.value.id
    );
    
    if (unreadMessages.length === 0) return;
    
    const messageIds = unreadMessages.map(msg => msg.id);
    
    const response = await api.post("/chat/messages/mark_as_read/", {
      chat_id: chatroomId.value
    });
    console.log("Mensagens marcadas como lidas");
    
    // Atualizar status das mensagens localmente
    updateMessagesReadStatus(messageIds);
    
    // Emitir evento para atualizar o Main-Menu e remover animação
    const event = new CustomEvent('unread-messages-updated');
    window.dispatchEvent(event);
    
    // Emitir evento via socket para notificar o outro usuário sobre as mensagens lidas
    if (socket.value && socket.value.connected) {
      socket.value.emit('messages_read', {
        chat_id: chatroomId.value,
        message_ids: messageIds
      });
    }
  } catch (error) {
    console.error("Erro ao marcar mensagens como lidas:", error);
  }
};

// Marcar uma mensagem específica como lida
const markMessageAsRead = async (messageId) => {
  if (!chatroomId.value || !currentUser.value?.id) return;
  
  try {
    await api.post("/chat/messages/mark_as_read/", {
      chat_id: chatroomId.value,
      message_id: messageId
    });
    
    // Emitir evento via socket para notificar o outro usuário sobre a mensagem lida
    if (socket.value && socket.value.connected) {
      socket.value.emit('messages_read', {
        chat_id: chatroomId.value,
        message_ids: [messageId]
      });
    }
  } catch (error) {
    console.error(`Erro ao marcar mensagem ${messageId} como lida:`, error);
  }
};

// Atualizar localmente o status das mensagens
const updateMessagesReadStatus = (messageIds) => {
  messages.value = messages.value.map(msg => {
    if (messageIds.includes(msg.id)) {
      return { ...msg, is_read: true };
    }
    return msg;
  });
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

// Função para adicionar o emoji selecionado à mensagem
const addEmoji = (emoji) => {
  messageContent.value += emoji;
};

// Função para alternar a visibilidade do seletor de emojis
const toggleEmojiPicker = () => {
  showEmojiPicker.value = !showEmojiPicker.value;
  
  // Se o seletor estiver aberto, configuramos um listener de clique para fechá-lo quando clicar fora
  if (showEmojiPicker.value) {
    setTimeout(() => {
      window.addEventListener('click', closeEmojiPickerOnClickOutside);
    }, 100);
  } else {
    window.removeEventListener('click', closeEmojiPickerOnClickOutside);
  }
};

// Função para fechar o seletor de emojis quando clicar fora dele
const closeEmojiPickerOnClickOutside = (event) => {
  const emojiPickerElements = document.querySelectorAll('.emoji-picker-area');
  let clickedInside = false;
  
  emojiPickerElements.forEach(element => {
    if (element.contains(event.target)) {
      clickedInside = true;
    }
  });
  
  if (!clickedInside) {
    showEmojiPicker.value = false;
    window.removeEventListener('click', closeEmojiPickerOnClickOutside);
  }
};


// Quando o componente é montado
onMounted(async () => {
  await fetchCurrentUser();
  await fetchItem();
  await fetchReceiverId();
  await fetchChatroomData();
  await fetchMessages();
  connectWebSocket();
  
  // Garantir rolagem para o final mesmo após todas as operações assíncronas
  setTimeout(() => {
    scrollToBottom();
  }, 300);
  
  // Configurar atualização periódica do status das mensagens (a cada 5 segundos)
  // Isso serve como uma segurança caso o websocket não funcione
  const intervalId = setInterval(() => {
    if (messages.value.length > 0) {
      // Verificamos se há mensagens que enviamos e que ainda não estão marcadas como lidas
      const unreadSentMessages = messages.value.filter(
        msg => msg.sender === currentUser.value?.id && !msg.is_read
      );
      
      if (unreadSentMessages.length > 0) {
        fetchMessages(); // Atualiza o status de leitura
      }
    }
  }, 5000);
  
  // Limpeza
  return () => {
    clearInterval(intervalId);
    if (socket.value) {
      socket.value.disconnect();
    }
  };
});
</script>

<style scoped></style>