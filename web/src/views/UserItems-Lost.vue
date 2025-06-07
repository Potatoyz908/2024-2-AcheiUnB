<template>
  <div
    class="fixed w-full top-0 h-[100px] bg-verde shadow-md rounded-b-xl flex items-center justify-between px-6 text-white z-10"
  >
    <router-link to="/user" class="inline-block">
      <img
        src="../assets/icons/arrow-left-white.svg"
        alt="Voltar"
        class="w-[35px] h-[35px] text-white transform transition duration-300 hover:scale-125"
      />
    </router-link>

    <h1 class="text-2xl font-bold absolute left-1/2 transform -translate-x-1/2">Meus Itens</h1>

    <button>
      <router-link to="/about" class="no-underline text-white">
        <Logo class="pr-4" sizeClass="text-2xl" />
      </router-link>
    </button>
  </div>

  <div class="pb-8 pt-24">
    <SubMenu />
  </div>

  <EmptyState
    v-if="myItemsLost.length === 0"
    message="perdidos registrados... Você pode adicionar um no"
    highlightText="AcheiUnB"
  />

  <div
    v-else
    class="grid grid-cols-[repeat(auto-fit,_minmax(180px,_1fr))] sm:grid-cols-[repeat(auto-fit,_minmax(200px,_1fr))] justify-items-center align-items-center lg:px-3 gap-y-3 pb-24"
  >
    <ItemCard
      v-for="item in paginatedItems"
      :key="item.id"
      :id="item.id"
      :name="item.name"
      :location="item.location_name"
      :time="formatTime(item.created_at)"
      :image="item.image_urls[0] || NotAvailableImage"
      :isMyItem="true"
      @delete="confirmDelete"
      @edit="handleEdit"
    />
  </div>

  <div v-if="myItemsLost.length" class="flex w-full justify-center pb-24">
    <div class="flex gap-4 z-0 items-center">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="1.5"
        stroke="currentColor"
        class="size-10 text-azul hover:text-laranja transition duration-200 cursor-pointer hover:scale-125"
        @click="goToPreviousPage"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="m11.25 9-3 3m0 0 3 3m-3-3h7.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
        />
      </svg>
      <span class="font-medium text-base text-azul select-none min-w-[30px] text-center">
        {{ currentPage }} / {{ totalPages }}
      </span>
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="1.5"
        stroke="currentColor"
        class="size-10 text-azul hover:text-laranja transition duration-200 cursor-pointer hover:scale-125"
        @click="goToNextPage"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="m12.75 15 3-3m0 0-3-3m3 3h-7.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
        />
      </svg>
    </div>
  </div>

  <ButtonAdd />

  <div class="fixed bottom-0 w-full">
    <MainMenu activeIcon="search" />
  </div>

  <Alert v-if="submitError" type="error" :message="alertMessage" @closed="submitError = false" />
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { fetchMyItemsLost, deleteItem } from "@/services/apiItems";
import { formatTime } from "@/utils/dateUtils";
import MainMenu from "../components/Main-Menu.vue";
import SubMenu from "../components/Sub-Menu-UserLost.vue";
import ItemCard from "@/components/Item-Card.vue";
import Alert from "@/components/Alert.vue";
import Logo from "@/components/Logo.vue";
import NotAvailableImage from "@/assets/images/not-available.png";
import EmptyState from "@/components/Empty-State-User.vue";

const router = useRouter();

const myItemsLost = ref([]);
const submitError = ref(false);
const formSubmitted = ref(false);
const alertMessage = ref("");
const loading = ref(true);
const currentPage = ref(1);
const itemsPerPage = 27;
const totalPages = computed(() => Math.max(1, Math.ceil(myItemsLost.value.length / itemsPerPage)));
const paginatedItems = computed(() => myItemsLost.value.slice((currentPage.value-1)*itemsPerPage, currentPage.value*itemsPerPage));

const fetchItems = async () => {
  try {
    const response = await fetchMyItemsLost();
    myItemsLost.value = response;
  } catch (error) {
    alertMessage.value = "Erro ao carregar itens perdidos.";
    submitError.value = true;
  }

  loading.value = false;
};

const confirmDelete = async (itemId) => {
  try {
    await deleteItem(itemId);
    myItemsLost.value = myItemsLost.value.filter((item) => item.id !== itemId);
  } catch (error) {
    console.error("Erro ao excluir item:", error);
    alertMessage = "Erro ao excluir item.";
    submitError = true;
  }
};

const handleDelete = async (itemId) => {
  try {
    await deleteItem(itemId);
    myItemsLost.value = myItemsLost.value.filter((item) => item.id !== itemId);
    alertMessage.value = "Item deletado com sucesso.";
    formSubmitted.value = true;
  } catch (error) {
    alertMessage.value = "Erro ao deletar o item.";
    submitError.value = true;
  }
};

const goToPreviousPage = () => {
  if (currentPage.value > 1) currentPage.value--;
};
const goToNextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++;
};

const handleEdit = (itemId) => {
  router.push(`/edit-item/${itemId}`);
};

onMounted(() => fetchItems());
</script>

<style scoped></style>
