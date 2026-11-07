/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{ts,tsx,js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: '#2D5A27', light: '#4A7C44', dark: '#1B3A17' },
        surface: { DEFAULT: '#F8FAFC', card: '#FFFFFF' },
        text: { DEFAULT: '#1E293B', secondary: '#64748B' },
        accent: '#D97706',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        card: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
      },
    },
  },
  plugins: [],
}