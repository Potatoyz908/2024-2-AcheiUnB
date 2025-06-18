<template>
  <div class="fixed bottom-[80px] right-6 z-10">
    <router-link
      :to="statusRoute"
      class="bg-laranja rounded-full w-16 h-16 flex items-center justify-center shadow-xl hover:scale-110 transition-transform duration-300"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="2.5"
        stroke="white"
        class="w-8 h-8"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M12 4.5v15m7.5-7.5h-15"
        />
      </svg>
    </router-link>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

// Determine qual rota usar com base na URL atual
const statusRoute = computed(() => {
  if (route.path.includes('user-items-lost')) {
    return '/register-lost';
  } else if (route.path.includes('user-items-found')) {
    return '/register-found';
  } else {
    // Caso padrão, pode ser modificado conforme necessário
    return '/register-lost';
  }
});
</script>
