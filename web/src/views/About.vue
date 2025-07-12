<template>
  <div class="relative min-h-screen">
    <div
      class="absolute inset-0 bg-no-repeat bg-cover bg-center opacity-10 z-[-1]"
      :style="{
        backgroundImage: `url(${backgroundImage})`,
        backgroundSize: isLargeScreen ? '50%' : 'contain',
        backgroundAttachment: 'fixed',
      }"
    ></div>
    <div class="fixed w-full top-0" style="z-index: 1">
      <AboutHeader />
    </div>
    <div class="pt-[120px] flex justify-center my-6 text-azul">
      <Logo />
    </div>
    <span
      class="font-inter text-azul mx-auto max-w-xl sm:px-12 px-12 md:max-w-2xl mt-7 text-center block"
    >
      Somos um grupo da disciplina <strong>Métodos de Desenvolvimento de Software</strong> da UnB.
      <br />
      Nosso objetivo é resolver um dos desafios enfrentados na faculdade: a falta de uma ferramenta
      eficiente para organizar itens <strong>achados e perdidos</strong> pelos estudantes.
      <br /><br />
      <!-- Adiciona um espaço extra -->
      <strong>Com o AcheiUnB</strong>, você pode, de forma simples e intuitiva, buscar por um item
      perdido ou cadastrar algo que encontrou, ajudando a nossa
      <strong>comunidade acadêmica</strong>.
    </span>

    <div class="flex justify-center mt-6 px-10">
      <button
        class="bg-laranja text-white w-full md:w-[70%] lg:w-[40%] font-medium py-4 rounded-full hover:scale-110 transition-transform duration-300 text-center text-lg lg:text-xl"
      >
        <a href="https://unb-mds.github.io/2024-2-AcheiUnB/CONTRIBUTING/" target="_blank">
          Como Contribuir?
        </a>
      </button>
    </div>

    <div class="max-w-4xl mx-auto mt-10 p-5 pb-[140px]">
      <div class="text-azul text-lg text-center font-semibold mb-7">Criado por:</div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="creator in creators" :key="creator.name" class="flex flex-col items-center">
          <a :href="creator.github" target="_blank">
            <img
              :src="creator.image"
              :alt="creator.name"
              class="w-[100px] rounded-full hover:scale-110 transition-transform"
            />
          </a>
          <div class="text-center mt-2">
            <p class="font-inter font-medium">{{ creator.name }}</p>
            <p class="text-sm text-cinza3">Engenharia de Software</p>
          </div>
        </div>
      </div>
    </div>

    <ButtonAdd />
    <div class="fixed bottom-0 w-full">
      <MainMenu activeIcon="info" />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import AboutHeader from "../components/Header-About.vue";
import MainMenu from "../components/Main-Menu.vue";
import Logo from "../components/Logo.vue";
import backgroundImagePath from "@/assets/icons/Favicon2.png";

const backgroundImage = ref(backgroundImagePath);

const creators = [
  {
    name: "Ana Elisa Ramos",
    github: "https://github.com/anaelisaramos",
    image: "https://github.com/anaelisaramos.png",
  },
  {
    name: "Davi Camilo",
    github: "https://github.com/DaviCamilo23",
    image: "https://github.com/DaviCamilo23.png",
  },
  {
    name: "Euller Júlio da Silva",
    github: "https://github.com/potatoyz908",
    image: "https://github.com/potatoyz908.png",
  },
  {
    name: "Leonardo Ramiro",
    github: "https://github.com/leoramiroo",
    image: "https://github.com/leoramiroo.png",
  },
  {
    name: "Pedro Everton",
    github: "https://github.com/pedroeverton217",
    image: "https://github.com/pedroeverton217.png",
  },
  {
    name: "Pedro Martins Silva",
    github: "https://github.com/314dro",
    image: "https://github.com/314dro.png",
  },
  {
    name: "Tiago Balieiro",
    github: "https://github.com/TiagoBalieiro",
    image: "https://github.com/TiagoBalieiro.png",
  },
];
</script>

<style scoped></style>
