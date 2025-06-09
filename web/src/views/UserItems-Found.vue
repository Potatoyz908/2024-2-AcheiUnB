<template>
 <div class="fixed w-full top-0 z-10">
    <HeaderUserItem />
  </div>

  <div class="pb-8 pt-24">
    <SubMenu />
  </div>

  <EmptyState
    v-if="myItemsFound.length === 0"
    message="achados registrados... Você pode adicionar um no"
    highlightText="AcheiUnB"
  />

  <div
    v-else
    class="grid grid-cols-[repeat(auto-fit,_minmax(180px,_1fr))] sm:grid-cols-[repeat(auto-fit,_minmax(200px,_1fr))] justify-items-center align-items-center lg:px-3 gap-y-3 pb-24"
  >
    <ItemCard
      v-for="item in myItemsFound"
      :key="item.id"
      :id="item.id"
      :name="item.name"
      :location="item.location_name"
      :time="formatTime(item.created_at)"
      :image="item.image_urls[0] || NotAvailableImage"
      :isMyItem="true"
      @delete="confirmDelete"
    />
  </div>

  <ButtonAdd />
  <div class="fixed bottom-0 w-full">
    <MainMenu activeIcon="search" />
  </div>

  <Alert v-if="submitError" type="error" :message="alertMessage" @closed="submitError = false" />
</template>

<script setup>
import { ref, onMounted } from "vue";
import { fetchMyItemsFound, deleteItem } from "@/services/apiItems";
import { formatTime } from "@/utils/dateUtils";
import MainMenu from "../components/Main-Menu.vue";
import SubMenu from "../components/Sub-Menu-UserFound.vue";
import ItemCard from "@/components/Item-Card.vue";
import HeaderUserItem from "../components/Header-UserItem.vue";
import Logo from "@/components/Logo.vue";
import NotAvailableImage from "@/assets/images/not-available.png";
import EmptyState from "@/components/Empty-State-User.vue";

const myItemsFound = ref([]);
const submitError = ref(false);
const formSubmitted = ref(false);
const alertMessage = ref("");
const loading = ref(true);

const fetchItems = async () => {
  try {
    const response = await fetchMyItemsFound();
    myItemsFound.value = response;
  } catch (error) {
    alertMessage.value = "Erro ao carregar itens encontrados.";
    submitError.value = true;
  }

  loading.value = false;
};

const confirmDelete = async (itemId) => {
  try {
    await deleteItem(itemId);
    myItemsFound.value = myItemsFound.value.filter((item) => item.id !== itemId);
  } catch (error) {
    console.error("Erro ao excluir item:", error);
    alertMessage.value = "Erro ao excluir item.";
    submitError.value = true;
  }
};

const handleDelete = async (itemId) => {
  try {
    await deleteItem(itemId);
    myItemsFound.value = myItemsFound.value.filter((item) => item.id !== itemId);
    alertMessage.value = "Item deletado com sucesso.";
    formSubmitted.value = true;
  } catch (error) {
    alertMessage.value = "Erro ao deletar o item.";
    submitError.value = true;
  }
};

onMounted(() => fetchItems());
</script>

<style scoped></style>
