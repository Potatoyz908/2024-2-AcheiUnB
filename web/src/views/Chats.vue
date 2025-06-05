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

  <div v-else-if="chatrooms.length" class="pt-32 pb-24">
    <div
      v-for="chatroom in chatrooms"
      :key="chatroom.id"
      class="flex items-center px-6 py-5 cursor-pointer transition-all duration-200 hover:bg-gray-200"
      @click="openChat(chatroom)"
    >
      <img
        :src="chatroom.recipient.foto"
        alt="Foto do usuário"
        class="w-16 h-16 md:w-20 md:h-20 rounded-full object-cover border-2 border-white"
      />

      <div class="ml-5">
        <p class="text-xl font-semibold text-gray-800">{{ chatroom.recipient.name }}</p>
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
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";
import ItemHeader from "../components/Item-Header.vue";
import MainMenu from "../components/Main-Menu.vue";
import defaultAvatar from "@/assets/images/default-avatar.png";
import Alert from "@/components/Alert.vue";

const router = useRouter();
const currentUser = ref(null);
const chatrooms = ref([]);
const loadingChats = ref(true);
const alertMessage = ref("");
const submitError = ref(false);

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

async function fetchCurrentUser() {
  try {
    const response = await api.get(`/auth/user/`);
    currentUser.value = response.data;
    await fetchUserChatrooms();
  } catch (error) {
    console.error("Erro ao buscar usuário:", error);
    alertMessage.value = "Erro ao buscar usuário.";
    submitError.value = true;
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

        chatroomsTemp.push({
          ...chatroom,
          recipient: {
            id: otherUserId,
            name: otherUserName,
            foto: otherUserFoto,
          },
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

onMounted(() => {
  fetchCurrentUser();
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
