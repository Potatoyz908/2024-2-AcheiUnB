<template>
  <div
    class="w-full h-[100px] bg-verde shadow-md rounded-b-xl grid grid-cols-[1fr_2fr_1fr] items-center px-4 text-white"
  >
    <!-- Coluna da esquerda: botão voltar -->
    <router-link to="/user" class="flex justify-start">
      <img
        src="@/assets/icons/arrow-left-white.svg"
        alt="Voltar"
        class="w-[30px] h-[30px] hover:scale-125 transition-transform"
      />
    </router-link>

    <!-- Coluna central: título -->
    <div class="text-center">
      <h1 class="text-2xl sm:text-2xl md:text-3xl font-bold">Meus Itens</h1>
    </div>

    <!-- Coluna da direita: logo -->
    <router-link to="/about" class="flex justify-end pr-0 md:pr-4">
    <Logo sizeClass="text-xl sm:text-2xl md:text-2xl" />
    </router-link>

  </div>
</template>

<script>
import Logo from "./Logo.vue";

export default {
    name: "Header-UserItem",
    components: {
        Logo
  }
};
</script>