/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'breizhblue': {
          50: '#f0f7ff',
          100: '#e0eefe',
          200: '#bae0fd',
          300: '#7cc8fc',
          400: '#38aaf7',
          500: '#0e8fe9',
          600: '#0072c7',
          700: '#0059a2',
          800: '#064b85',
          900: '#0a3f6f',
        }
      }
    },
  },
  plugins: [],
}
