<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
    <div class="bg-white rounded-lg shadow-xl w-11/12 max-w-md p-6 md:p-8">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl md:text-2xl font-bold text-azul">Reportar um Problema</h2>
        <button @click="closeModal" class="text-gray-500 hover:text-gray-700">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <form @submit.prevent="submitReport">
        <div class="mb-4">
          <label for="subject" class="block text-gray-700 text-sm font-medium mb-2">Assunto</label>
          <input
            id="subject"
            v-model="subject"
            type="text"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-azul"
            placeholder="Digite o assunto do problema"
            required
          />
        </div>

        <div class="mb-4">
          <label for="description" class="block text-gray-700 text-sm font-medium mb-2">Descrição</label>
          <textarea
            id="description"
            v-model="description"
            rows="4"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-azul"
            placeholder="Descreva o problema em detalhes"
            required
          ></textarea>
        </div>

        <div class="mb-6">
          <label for="attachment" class="block text-gray-700 text-sm font-medium mb-2">Anexo (opcional)</label>
          <div class="flex items-center justify-center w-full">
            <label
              for="attachment"
              class="flex flex-col items-center justify-center w-full h-24 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100"
            >
              <div class="flex flex-col items-center justify-center pt-5 pb-6">
                <svg
                  class="w-8 h-8 mb-2 text-gray-500"
                  aria-hidden="true"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 20 16"
                >
                  <path
                    stroke="currentColor"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
                  />
                </svg>
                <p class="text-sm text-gray-500">
                  <span v-if="!fileName">Clique para adicionar um anexo</span>
                  <span v-else>{{ fileName }}</span>
                </p>
              </div>
              <input
                id="attachment"
                type="file"
                @change="handleFileChange"
                class="hidden"
              />
            </label>
          </div>
        </div>

        <div class="flex justify-end space-x-3">
          <button
            type="button"
            @click="closeModal"
            class="px-4 py-2 rounded-lg text-gray-700 hover:bg-gray-100"
          >
            Cancelar
          </button>
          <button
            type="submit"
            class="px-4 py-2 bg-azul text-white rounded-lg hover:bg-azul/90 disabled:opacity-50"
            :disabled="isSubmitting"
          >
            {{ isSubmitting ? 'Enviando...' : 'Enviar' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '@/services/api';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  userEmail: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['close', 'success', 'error']);

const subject = ref('');
const description = ref('');
const attachment = ref(null);
const fileName = ref('');
const isSubmitting = ref(false);

function closeModal() {
  subject.value = '';
  description.value = '';
  attachment.value = null;
  fileName.value = '';
  emit('close');
}

function handleFileChange(event) {
  const file = event.target.files[0];
  if (file) {
    attachment.value = file;
    fileName.value = file.name;
  } else {
    attachment.value = null;
    fileName.value = '';
  }
}

async function submitReport() {
  try {
    isSubmitting.value = true;
    
    const formData = new FormData();
    formData.append('subject', subject.value);
    formData.append('message', description.value);
    formData.append('from_email', props.userEmail);
    
    if (attachment.value) {
      formData.append('attachment', attachment.value);
    }
    
    await api.post('/support/report-problem/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      }
    });

    isSubmitting.value = false;
    emit('success', 'Problema reportado com sucesso!');
    closeModal();
  } catch (error) {
    console.error('Erro ao enviar o relatório:', error);
    isSubmitting.value = false;
    emit('error', 'Ocorreu um erro ao reportar o problema. Tente novamente.');
  }
}
</script>
