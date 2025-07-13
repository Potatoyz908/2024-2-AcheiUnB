<template>
  <div
    class="h-[100px] bg-verde shadow-md rounded-b-xl flex items-center justify-start text-white gap-x-9 p-6"
    :class="{ visible: isVisible, invisible: !isVisible }"
  >
    <router-link to="/lost" class="inline-block">
      <img
        src="../assets/icons/arrow-left-white.svg"
        alt="Voltar"
        class="w-[35px] h-[35px] text-white transform transition duration-300 hover:scale-125"
      />
    </router-link>
    <div class="flex-1 text-center">
      <span class="font-inter font-semibold text-lg sm:text-2xl">{{
        text ?? "Cadastro de item perdido"
      }}</span>
    </div>
    <button class="ml-auto">
      <router-link to="/about" class="no-underline text-white">
        <Logo class="transform translate-y-[1.25px] pr-4" sizeClass="text-xl sm:text-2xl" />
      </router-link>
    </button>
  </div>
</template>

<script>
import Logo from "./Logo.vue";

export default {
  name: "LostHeader",
  data() {
    return {
      isVisible: false,
    };
  },
  components: {
    Logo,
  },
  props: {
    text: String,
  },
  mounted() {
    setTimeout(() => {
      this.isVisible = true;
    }, 1);
  },
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
  transform: translateY(-45px);
}
</style>
