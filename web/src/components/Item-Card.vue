<template>
  <div
    class="w-[170px] sm:w-[190px] h-[230px] bg-cinza1 rounded-sm shadow-complete p-2 flex flex-col relative z-0 cursor-pointer transform transition duration-300 hover:scale-105"
    @click="!disabled ? viewItemDetails() : null"
  >
    <div class="w-full h-[120px] bg-cinza2 rounded-sm flex justify-center items-start">
      <img :src="image" class="rounded-sm w-full h-full max-w-full max-h-full object-cover" />
    </div>

    <button
      v-if="isMyItem"
      class="absolute p-1 bottom-2 border-2 border-laranja right-2 w-7 h-7 bg-white flex items-center justify-center text-xs rounded-full cursor-pointer"
      @click.stop="openModal(id)"
      title="Excluir"
    >
      <img src="../assets/icons/trash.svg" alt="Excluir" />
    </button>
    
    <button
      v-if="isMyItem"
      class="absolute p-1 bottom-2 border-2 border-azul right-12 w-7 h-7 bg-white flex items-center justify-center text-xs rounded-full cursor-pointer"
      @click.stop="emit('edit', id)"
      title="Editar"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-azul">
        <path d="M11.5 4.5L14 2L12 0L9.5 2.5M11.5 4.5L4.5 11.5L2 14L0 12L2.5 9.5M11.5 4.5L9.5 2.5M2.5 9.5L9.5 2.5" />
      </svg>
    </button>

    <Teleport to="body">
      <div
        v-if="showConfirmModal"
        class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
      >
        <div
          class="bg-azul p-6 rounded-lg shadow-lg w-full max-w-sm sm:max-w-md lg:max-w-lg text-center relative"
          @click.stop
        >
          <p class="text-white font-inter text-lg">
            Você realmente deseja excluir este item do AcheiUnB?
          </p>

          <div class="flex flex-col sm:flex-row justify-center mt-4 gap-4">
            <button
              class="bg-red-500 text-white font-inter px-4 py-2 rounded-md hover:bg-red-600 transition w-full sm:w-auto"
              @click="confirmDelete"
            >
              Excluir
            </button>
            <button
              class="bg-white font-inter px-4 py-2 rounded-md hover:bg-gray-200 transition w-full sm:w-auto"
              @click="closeModal"
            >
              Cancelar
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <div class="h-[2px] w-1/4 bg-laranja mt-4"></div>

    <!--textos-->
    <div class="flex flex-col" :class="{'pr-14': isMyItem}">
      <div class="text-azul font-bold font-inter mt-1 truncate">{{ name }}</div>
      <div class="flex items-start justify-start overflow-hidden">
        <img src="../assets/icons/locale.svg" alt="" class="w-5 h-5 mr-1 flex-shrink-0" />
        <span class="text-azul font-inter text-md font-medium truncate">{{ location }}</span>
      </div>
    </div>

    <span
      class="text-right font-inter font-bold text-xs text-cinza3 p-1 flex justify-end items-center"
    >
      <template v-if="!isMyItem">
        {{ time }}
      </template>
    </span>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import { useRouter } from "vue-router";

const props = defineProps({
  id: Number,
  image: String,
  name: String,
  time: String,
  location: String,
  isMyItem: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["delete", "edit"]);
const router = useRouter();
const showConfirmModal = ref(false);
const selectedItemId = ref(null);

const viewItemDetails = () => {
  if (!showConfirmModal.value) {
    router.push({ name: "ListItem", query: { idItem: props.id } });
  }
};

const openModal = (id) => {
  selectedItemId.value = id;
  showConfirmModal.value = true;

  // Bloqueia a rolagem da página quando o modal está aberto
  document.body.style.overflow = "hidden";
};

const closeModal = () => {
  showConfirmModal.value = false;
  selectedItemId.value = null;

  // Libera a rolagem da página ao fechar o modal
  document.body.style.overflow = "";
};

const confirmDelete = () => {
  emit("delete", props.id);
  showConfirmModal.value = false;
  closeModal();
};
</script>

<style scoped></style>
