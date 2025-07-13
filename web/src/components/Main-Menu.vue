<template>
  <div
    class="h-full bg-azul shadow-md rounded-t-xl flex items-center justify-center text-white gap-x-9 p-8 md:gap-x-9 md:p-4 lg:p-5 lg:gap-x-10"
    :class="{ visible: isVisible, invisible: !isVisible }"
  >
    <router-link to="/found" class="no-underline flex flex-col items-center group">
      <svg 
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="1.5"
        stroke="currentColor"
        class="size-6 md:size-7 lg:size-8 group-hover:text-laranja hover:cursor-pointer"
        :class="{ 'text-laranja': activeIcon == 'search' }"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"
        />
      </svg>
      <span class="hidden md:block text-xs lg:text-sm font-medium mt-1 group-hover:text-laranja" :class="{ 'text-laranja': activeIcon == 'search' }">
        {{ currentRoute.includes('/lost') ? 'Perdidos' : 'Achados' }}
      </span>
    </router-link>

    <router-link to="/user" class="no-underline flex flex-col items-center group">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="1.5"
        stroke="currentColor"
        class="size-6 md:size-7 lg:size-8 group-hover:text-laranja hover:cursor-pointer"
        :class="{ 'text-laranja': activeIcon == 'user' }"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z"
        />
      </svg>
      <span class="hidden md:block text-xs lg:text-sm font-medium mt-1 group-hover:text-laranja" :class="{ 'text-laranja': activeIcon == 'user' }">Perfil</span>
    </router-link>

    <router-link to="/about" class="no-underline flex flex-col items-center group">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="1.5"
        stroke="currentColor"
        class="size-6 md:size-7 lg:size-8 group-hover:text-laranja hover:cursor-pointer"
        :class="{ 'text-laranja': activeIcon == 'info' }"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z"
        />
      </svg>
      <span class="hidden md:block text-xs lg:text-sm font-medium mt-1 group-hover:text-laranja" :class="{ 'text-laranja': activeIcon == 'info' }">Sobre</span>
    </router-link>

    <router-link to="/chats" class="no-underline flex flex-col items-center group relative">
      <div class="relative">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="size-6 md:size-7 lg:size-8 group-hover:text-laranja hover:cursor-pointer"
          :class="{ 
            'text-laranja': activeIcon == 'chat'
          }"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M8.625 12a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H8.25m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H12m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 0 1-2.555-.337A5.972 5.972 0 0 1 5.41 20.97a5.969 5.969 0 0 1-.474-.065 4.48 4.48 0 0 0 .978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25Z"
          />
        </svg>
        <span v-if="hasUnreadMessages" 
              class="absolute -top-1 -right-1 flex h-3 w-3">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-laranja opacity-75"></span>
          <span class="relative inline-flex rounded-full h-3 w-3 bg-laranja"></span>
        </span>
      </div>
      <span class="hidden md:block text-xs lg:text-sm font-medium mt-1 group-hover:text-laranja" 
            :class="{ 'text-laranja': activeIcon == 'chat' }">
        Conversas
      </span>
    </router-link>
  </div>
</template>

<script>
import api from '@/services/api';
import { useRoute } from 'vue-router';
import { computed, ref } from 'vue';

export default {
  name: "MainMenu",
  props: {
    activeIcon: String,
  },
  setup() {
    const route = useRoute();
    const currentRoute = computed(() => route.path);
    
    return {
      currentRoute
    };
  },
  data() {
    return {
      isVisible: false,
      hasUnreadMessages: false,
    };
  },
  mounted() {
    setTimeout(() => {
      this.isVisible = true;
    }, 1);
    
    this.checkUnreadMessages();
    
    this.intervalId = setInterval(this.checkUnreadMessages, 60000);
    
    window.addEventListener('unread-messages-updated', this.checkUnreadMessages);
  },
  
  beforeUnmount() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
    
    window.removeEventListener('unread-messages-updated', this.checkUnreadMessages);
  },
  
  methods: {
    async checkUnreadMessages() {
      try {
        const response = await api.get("/chat/chatrooms/unread_messages/");
        this.hasUnreadMessages = response.data.unread_count > 0;
      } catch (error) {
        console.error("Erro ao verificar mensagens não lidas:", error);
      }
    }
  }
};
</script>

<style scoped>
.visible {
  opacity: 1;
  transform: translateY(0);
  transition:
    opacity 0.3s ease-in-out,
    transform 0.3s ease-in-out;
}

.invisible {
  opacity: 0;
  transform: translateY(45px);
}

@media (min-width: 770px) {
  .no-underline {
    width: 75px;
    min-width: 75px;
    text-align: center;
  }
  
  /* Garantindo que o texto não quebre e mantenha sua largura */
  .no-underline span {
    white-space: nowrap;
    display: block;
  }
  
  /* Mantenha o espaçamento entre os botões fixo */
  div.flex {
    gap: 2.5rem !important;
  }
}
@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.animate-bounce {
  animation: bounce 1s infinite;
}

@keyframes ping {
  75%, 100% {
    transform: scale(2);
    opacity: 0;
  }
}
</style>
