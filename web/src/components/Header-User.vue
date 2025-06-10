<template>
  <div
    class="h-[100px] bg-verde shadow-md rounded-b-xl flex items-center justify-between text-white px-6 py-4"
    :class="{ visible: isVisible, invisible: !isVisible }"
  >
    <div class="w-1/4 flex items-center">
      <!-- Botão de Voltar -->
      <img
        @click="goBack"
        :src="LeftArrow"
        alt="Voltar"
        class="w-[35px] h-35[px] md:w-8 md:h-8 lg:w-50 lg:w-50 cursor-pointer transform transition duration-300 hover:scale-125"
      />
    </div>
    <div class="w-2/4 text-center">
      <span class="font-inter font-semibold text-lg sm:text-2xl">
        {{ text ? text : "Meu Perfil" }}
      </span>
    </div>
    <div class="w-1/4 flex justify-end">
      <router-link to="/about" class="no-underline text-white">
        <Logo sizeClass="text-xl sm:text-2xl" />
      </router-link>
    </div>
  </div>
</template>

<script>
import Logo from "./Logo.vue";
import LeftArrow from "@/assets/icons/arrow-left-white.svg";
import { useRouter } from "vue-router";

export default {
  name: "UserHeader",
  components: {
    Logo,
  },
  props: {
    text: String,
  },
  setup() {
    const router = useRouter();
    
    const goBack = () => {
      router.back();
    };
    
    return {
      goBack,
      LeftArrow
    };
  },
  data() {
    return {
      isVisible: false,
    };
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
