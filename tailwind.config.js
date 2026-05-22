/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        washi: "#f4ecdb",
        washiDeep: "#ebe0c5",
        sumi: "#1f1d1a",
        shu: "#b6313a",
        shuDeep: "#7d1a23",
        ai: "#1d3b73",
        aiLight: "#3a5a92",
        kun: "#d97a8a",
        sou: "#7fb2d6",
        jun: "#c48a3a",
        juku: "#6b4423",
        other: "#9a958a",
      },
      fontFamily: {
        serif: ['"Noto Serif KR"', 'serif'],
        sans: ['"Noto Sans KR"', 'sans-serif'],
        deco: ['"Shippori Mincho"', '"Noto Serif KR"', 'serif'],
      },
    },
  },
  plugins: [],
};
