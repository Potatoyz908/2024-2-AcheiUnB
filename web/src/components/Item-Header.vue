<template>
  <div
    class="h-[100px] bg-verde shadow-md rounded-b-xl flex items-center text-white p-4 md:p-6"
    :class="{ visible: isVisible, invisible: !isVisible }"
  >
    <div class="flex items-center w-1/4">
      <img
        @click="goBack"
        src="../assets/icons/arrow-left-white.svg"
        alt="Voltar"
        class="w-[35px] h-[35px] text-white cursor-pointer hover:scale-110 transition-transform duration-300 hover:text-laranja"
      />
    </div>

    <div class="flex-grow flex justify-center">
      <span class="font-inter font-semibold text-2xl text-center break-words">
        {{ title }}
      </span>
    </div>

    <button
      v-if="userId === itemUserId && canEditUser"
      type="button"
      @click="editItem()"
      class="flex items-center w-1/4 justify-end hover:scale-90 transition-transform duration-300 pr-4"
    >
      <img
        src="@/assets/icons/EditarPerfil.svg"
        alt="Editar Item"
        class="w-[30px] h-[30px] text-white cursor-pointer"
      />
    </button>

    <div v-else class="flex items-center w-1/4 justify-end">
      <router-link to="/about" class="no-underline text-white">
        <Logo class="transform translate-y-[1.25px] md:pr-4" sizeClass="text-xl md:text-2xl" />
      </router-link>
    </div>
  </div>
</template>

<script>
import Logo from "./Logo.vue";

export default {
  name: "ItemHeader",
  components: {
    Logo,
  },
  data() {
    return {
      isVisible: false,
    };
  },
  props: {
    title: {
      type: String,
      required: true,
    },
    userId: {
      type: Number,
    },
    itemUserId: {
      type: Number,
    },
    itemId: {
      type: [String, Number],
    },
    canEditUser: {
      type: Boolean,
      default: true,
    },
  },
  methods: {
    goBack() {
      this.$router.back();
    },

    editItem() {
      this.$router.push(`/edit-item/${this.itemId}`);
    },
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
