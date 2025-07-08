<template>
  <form
    class="absolute flex items-center"
    :class="{
      'fixed w-full top-6 pr-8 z-50': isActive && !isMediumOrLarger,
      'relative w-auto': !isActive || isMediumOrLarger,
    }"
  >
    <button
      @click="
        toggleFilters();
        toggleActive();
      "
      class="absolute left-3 text-gray-500 hover:text-gray-700 transition-colors z-50"
      type="button"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="1.5"
        stroke="currentColor"
        class="size-6"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M10.5 6h9.75M10.5 6a1.5 1.5 0 1 1-3 0m3 0a1.5 1.5 0 1 0-3 0M3.75 6H7.5m3 12h9.75m-9.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-3.75 0H7.5m9-6h3.75m-3.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-9.75 0h9.75"
        />
      </svg>
    </button>
    <input
      v-model="filtersState.searchQuery"
      class="input bg-gray-200 rounded-full px-10 py-2 my-1 border-2 border-transparent focus:outline-none focus:border-laranja placeholder-gray-500 text-gray-700 transition-all duration-300 shadow-md pr-10 w-full z-40"
      :placeholder="animatedPlaceholder"
      type="text"
      @input="setSearchQuery(filtersState.searchQuery)"
      @focus="isActive = true"
      @blur="
        isActive = false;
        showFilters = false;
      "
    />
    <button
      class="absolute right-4 top-1/2 -translate-y-1/2 p-1 text-gray-400 hover:text-gray-600 transition-colors duration-200 z-50"
      :class="{
        'pr-8': isActive && !isMediumOrLarger,
      }"
      type="submit"
    >
      <svg
        width="17"
        height="16"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        role="img"
        aria-labelledby="search"
        class="w-5 h-5"
      >
        <path
          d="M7.667 12.667A5.333 5.333 0 107.667 2a5.333 5.333 0 000 10.667zM14.334 14l-2.9-2.9"
          stroke="currentColor"
          stroke-width="1.333"
          stroke-linecap="round"
          stroke-linejoin="round"
        ></path>
      </svg>
    </button>

    <div
      v-if="showFilters"
      class="absolute left-0 bg-gray-200 shadow-lg rounded-xl p-4 z-30 overflow-y-auto max-h-[670px]"
      :class="{
        'w-fit mr-8': isActive && !isMediumOrLarger,
        'w-full': isMediumOrLarger,
      }"
      style="top: calc(50% - 4px)"
    >
      <div class="flex gap-2 flex-wrap mt-4">
        <span class="w-full text-azul text-2xl font-bold">Categoria </span>
        <button
          type="button"
          v-for="(filter, index) in categories"
          :key="index"
          @click="setActiveCategory(filter.label)"
          :class="[
            'px-4 py-2 rounded-full border text-sm',
            filtersState.activeCategory === filter.label
              ? 'bg-laranja text-azul border-black'
              : 'bg-gray-200 text-azul border-black',
          ]"
        >
          {{ filter.label }}
        </button>
      </div>
      <div class="h-[2px] w-full bg-laranja mt-4"></div>
      <div class="flex gap-2 flex-wrap mt-4">
        <span class="w-full text-azul text-2xl font-bold">Local </span>
        <button
          type="button"
          v-for="(filter, index) in locations"
          :key="index"
          @click=" setActiveLocation(filter.label)"
          :class="[
            'px-4 py-2 rounded-full border text-sm',
            filtersState.activeLocation === filter.label
              ? 'bg-laranja text-azul border-black'
              : 'bg-gray-200 text-azul border-black',
          ]"
        >
          {{ filter.label }}
        </button>
      </div>
    </div>
  </form>
</template>

<script>
import {
  filtersState,
  setSearchQuery,
  setActiveCategory,
  setActiveLocation,
} from "@/store/filters";

export default {
  name: "SearchBar",

  setup() {
    return {
      filtersState,
      setSearchQuery,
      setActiveCategory,
      setActiveLocation,
    };
  },

  data() {
    return {
      fullPlaceholder: "Pesquise seu item",
      animatedPlaceholder: "",
      typingSpeed: 50,
      showFilters: false,
      isActive: false,
      categories: [
        { label: "Anel", active: false },
        { label: "Anotações", active: false },
        { label: "Apostila", active: false },
        { label: "Base", active: false },
        { label: "Batom", active: false },
        { label: "Blush", active: false },
        { label: "Blusa", active: false },
        { label: "Boné", active: false },
        { label: "Borracha", active: false },
        { label: "Calculadora", active: false },
        { label: "Calculadora Científica", active: false },
        { label: "Caneta", active: false },
        { label: "Carregador", active: false },
        { label: "Carregador Portátil", active: false },
        { label: "Carteira", active: false },
        { label: "Carteira de Identidade", active: false },
        { label: "Carteira de Motorista", active: false },
        { label: "Case Fone", active: false },
        { label: "Case Notebook", active: false },
        { label: "Casaco", active: false },
        { label: "Celular", active: false },
        { label: "Chapéu", active: false },
        { label: "Chaves", active: false },
        { label: "Chinelo", active: false },
        { label: "Caderno", active: false },
        { label: "Colar", active: false },
        { label: "Estojo", active: false },
        { label: "Fone de ouvido", active: false },
        { label: "Gloss", active: false },
        { label: "Grampeador", active: false },
        { label: "Guarda-chuva", active: false },
        { label: "Garrafa de Água", active: false },
        { label: "Lapiseira", active: false },
        { label: "Lápis", active: false },
        { label: "Lápis de olho", active: false },
        { label: "Livro", active: false },
        { label: "Mochila", active: false },
        { label: "Mouse", active: false },
        { label: "Necessaire", active: false },
        { label: "Notebook", active: false },
        { label: "Óculos", active: false },
        { label: "Passe Estudantil", active: false },
        { label: "Passe de Ônibus", active: false },
        { label: "Piercing", active: false },
        { label: "Pingente", active: false },
        { label: "Planner", active: false },
        { label: "Presilha de Cabelo", active: false },
        { label: "Pulseira", active: false },
        { label: "Relógio", active: false },
        { label: "Smartwatch", active: false },
        { label: "Stylus", active: false },
        { label: "Suporte Notebook", active: false },
        { label: "Sombra", active: false },
        { label: "Tablet", active: false },
        { label: "Touca", active: false },
        { label: "Outra", active: false },
      ],
      locations: [
        { label: "UAC", active: false },
        { label: "UED", active: false },
        { label: "LDTEA", active: false },
        { label: "RU", active: false },
        { label: "Containers", active: false },
        { label: "Diretório Acadêmico - DA", active: false },
        { label: "Quadra Poliesportiva", active: false },
        { label: "Guarita Estacionamento Sul", active: false },
        { label: "Guarita Estacionamento Norte", active: false },
        { label: "Outro", active: false },
      ],
    };
  },
  computed: {
    isMediumOrLarger() {
      return window.innerWidth >= 768;
    },
    searchQueryWithoutAccents() {
      return this.searchQuery
        ? this.searchQuery.normalize("NFD").replace(/[\u0300-\u036f]/g, "")
        : "";
    },
  },
  mounted() {
    this.startTypingEffect();
  },
  methods: {
    toggleActive() {
      this.isActive = !this.isActive;
    },

    toggleFilters() {
      this.showFilters = !this.showFilters;
    },

    toggleFilter(type, index) {
      if (type === "category") {
        this.categories.forEach((filter, i) => {
          if (i === index) {
            filter.active = !filter.active;
          } else {
            filter.active = false;
          }
        });
      } else if (type === "location") {
        this.locations.forEach((filter, i) => {
          if (i === index) {
            filter.active = !filter.active;
          } else {
            filter.active = false;
          }
        });
      }
    },

    startTypingEffect() {
      let index = 0;
      this.animatedPlaceholder = "";
      const interval = setInterval(() => {
        if (index < this.fullPlaceholder.length) {
          this.animatedPlaceholder += this.fullPlaceholder[index];
          index++;
        } else {
          clearInterval(interval);
        }
      }, this.typingSpeed);
    },
  },
};
</script>

<style scoped></style>
