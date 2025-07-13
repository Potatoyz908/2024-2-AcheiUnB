<template>
  <div
    class="h-[100px] bg-verde shadow-md rounded-b-xl flex items-center justify-between text-white p-6"
    :class="{ visible: isVisible, invisible: !isVisible }"
  >
    <img
      @click="goBack"
      :src="LeftArrow"
      alt="Voltar"
      class="w-[35px] h-[35px] md:w-8 md:h-8 cursor-pointer transform transition duration-300 hover:scale-125"
    />
    <div class="flex-1 flex justify-center">
      <span class="font-inter font-semibold text-2xl">
        {{ text ? text : "Sobre o projeto" }}
      </span>
    </div>
    <div style="width:35px"></div>
  </div>
</template>

<script>
import LeftArrow from "@/assets/icons/arrow-left-white.svg";
export default {
  name: "AboutHeader",
  props: {
    text: String,
  },
  data() {
    return {
      isVisible: false,
      LeftArrow,
    };
  },
  mounted() {
    setTimeout(() => {
      this.isVisible = true;
    }, 1);
  },
  methods: {
    goBack() {
      this.$router.back();
    },
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
