import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/globals.css",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}"
  ],
  theme: {
    extend: {
      colors: {
        background: '#f5faf6',
        foreground: '#1e2d2b',
        primary: '#2f9e44',
        accent: '#00aaff',
        card: '#ffffff',
        muted: '#e2e8f0',
        border: '#cbd5e1',
        success: '#28a745',
        warning: '#ffc107'
      },
      borderRadius: {
        DEFAULT: '0.75rem'
      },
      boxShadow: {
        DEFAULT: '0 4px 12px rgba(0,0,0,0.08)'
      }
    }
  },
  plugins: []
};

export default config;