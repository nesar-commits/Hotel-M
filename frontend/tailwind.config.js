/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        zomato: {
          DEFAULT: "#E23744",
          dark: "#CB202D",
          light: "#FFF1F1",
        },
      },
    },
  },
  plugins: [],
};
