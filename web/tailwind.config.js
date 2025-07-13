/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{vue,jsx}"],
  theme: {
    extend: {
      colors: {
        azul: "#133E78",
        laranja: "#F59E0B",
        verde: "#008940",
        cinza1: "#EAEAEA",
        cinza2: "#D9D9D9",
        cinza3: "#8899a8",
        vermelho: "#f63b3b",
      },
      boxShadow: {
        complete: "0 0 3px 1px rgb(0 0 0 / 0.1);",
      },
    },
    screens: {
      'sm': '640px',
      'md': '768px',
      'lg': '1024px',
      'xl': '1280px',
      'xxl': '1341px',
    },
  },
  plugins: [],
};
