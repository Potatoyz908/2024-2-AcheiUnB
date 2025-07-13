<template>
  <div
    class="w-full h-[100px] bg-verde shadow-md rounded-b-xl grid grid-cols-[1fr_2fr_1fr] items-center px-4 text-white"
  >
    <router-link to="/user" class="flex justify-start">
      <img
        src="@/assets/icons/arrow-left-white.svg"
        alt="Voltar"
        class="w-[35px] h-[35px] hover:scale-125 transition-transform"
      />
    </router-link>

    <div class="text-center">
      <h1 class="text-2xl sm:text-2xl md:text-3xl font-bold">Meus Itens</h1>
    </div>

    <router-link to="/about" class="flex justify-end items-center md:pr-4">
      <Logo class="transform translate-y-[1.25px]" sizeClass="text-xl sm:text-2xl md:text-2xl" />
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