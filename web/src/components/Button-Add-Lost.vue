<template>
  <router-link to="/register-lost">
    <button
      class="fixed right-0 bottom-28 rounded-l-xl custom-360:w-40 custom-360:h-12 w-48 h-14 sm:w-64 sm:h-16 md:w-80 md:h-20 cursor-pointer flex items-center border border-laranja bg-laranja group hover:bg-laranja active:bg-laranja active:border-laranja"
      :class="{ visible: isVisible, invisible: !isVisible }"
    >
      <span
        class="text-azul font-inter font-semibold text-xs sm:text-lg ml-4 sm:ml-12 transform group-hover:translate-x-0"
      >
        <span class="block max-[769px]:block min-[770px]:hidden">Adicionar perdido</span>
        <span class="hidden min-[770px]:block">Adicionar item perdido</span>
      </span>
      <span
        class="absolute right-0 h-12 w-10 sm:h-16 sm:w-10 md:h-20 md:w-10 rounded-xl bg-laranja flex items-center justify-center transform group-hover:translate-x-0 group-hover:w-full transition-all duration-300"
      >
        <img src="../assets/icons/add-item.svg" alt="" class="mr-4 sm:mr-10 w-6 h-6 sm:w-8 sm:h-8 md:w-10 md:h-10" />
      </span>
    </button>
  </router-link>
</template>

<script>
export default {
  props: {
    customClass: {
      name: "ButtonAdd",
      type: String,
    },
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
  transform: translateX(0);
  transition:
    opacity 0.5s ease-in-out,
    transform 0.5s ease-in-out;
}

.invisible {
  opacity: 0;
  transform: translateX(70px);
}

@media (max-width: 769px) and (min-width: 400px) {
  button {
    width: 16rem !important;
    height: 4rem !important;
  }
  .text-xs, .sm\:text-lg {
    font-size: 1.125rem !important;
    line-height: 1.75rem !important;
    margin-left: 2rem !important;
  }
  .h-12, .sm\:h-16 { height: 4rem !important; }
  .w-10, .sm\:w-10 { width: 2.5rem !important; }
  .mr-4, .sm\:mr-10 { margin-right: 3rem !important; }
  .w-6, .sm\:w-8 { width: 2rem !important; }
  .h-6, .sm\:h-8 { height: 2rem !important; }
}

@media (max-width: 799px) {
  .lg\:block { display: none !important; }
  .lg\:hidden { display: block !important; }
}
@media (min-width: 800px) {
  .lg\:block { display: block !important; }
  .lg\:hidden { display: none !important; }
}
@media (max-width: 399px) {
  button {
    width: 64px !important;
    height: 64px !important;
    font-size: 2.2rem !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
  }
  .text-azul, .font-inter, .font-semibold, .text-xs, .sm\:text-lg, .ml-4, .sm\:ml-12 {
    display: none !important;
  }
  .absolute.right-0 {
    position: static !important;
    margin: 0 !important;
    width: 100% !important;
    height: 100% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
  }
  img {
    margin: 0 !important;
    width: 2.2rem !important;
    height: 2.2rem !important;
    display: block !important;
  }
}
</style>
