<template>
  <div
    id="transition-screen"
    class="fixed inset-0 flex items-center justify-center z-50"
  >
    <div class="fixed inset-0 flex items-center justify-center z-50">
      <Logo customClass="text-azul" />
    </div>
  </div>

  <div
    id="main-content"
    class="telaInteira bg-azul text-white p-4 min-h-screen hidden"
  >
    <div
      class="titulo flex space-x-1 mt-20 mb-20 ml-8 md:flex md:justify-center md:mb-52"
    >
      <Logo />
    </div>
    <div
      class="slogan max-w-72 ml-8 md:mr-8 md:max-w-none md:w-auto md:text-center"
    >
      <p class="text-5xl font-bold mb-4 md:text-6xl">Perdeu algo no campus?</p>
      <p class="text-5xl italic font-light mb-4 md:text-6xl">
        A gente te ajuda!
      </p>
    </div>

    <div class="flex justify-center mt-52">
      <button
        @click="redirectToLoginMicrosoft"
        class="flex items-center rounded-full bg-gray-50 px-5 py-3 text-md font-medium text-azul ring-1 ring-inset ring-gray-500/10"
      >
        <img
          src="../assets/icons/Microsoft_logo2.svg"
          alt="Logo Microsoft"
          class="h-6 w-auto mr-2"
        />
        Entre com a conta da Microsoft
      </button>
    </div>
  </div>
</template>

<script setup>
import Logo from "../components/Logo.vue";

window.addEventListener("load", () => {
  const transitionScreen = document.getElementById("transition-screen");
  const mainContent = document.getElementById("main-content");

  setTimeout(() => {
    transitionScreen.classList.add("fade-out");
  }, 500);

  transitionScreen.addEventListener("animationend", () => {
    transitionScreen.classList.add("hidden");
    mainContent.classList.remove("hidden");
    mainContent.classList.add("fade-in");
  });
});

function redirectToLoginMicrosoft() {
  window.location.href =
    "https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=30194d95-b341-485e-8b37-cffcfc553414&scope=User.Read&response_type=code&state=Zay5NfY4tSn7JgvO&domain=alunos.unb.br";
}
</script>

<style scoped>
.fade-out {
  animation: fadeOut 1s forwards;
}

@keyframes fadeOut {
  0% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

.fade-in {
  animation: fadeIn 1s forwards;
}

@keyframes fadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
</style>
