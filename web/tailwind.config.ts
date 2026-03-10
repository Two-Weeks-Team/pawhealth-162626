import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/globals.css"
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--color-background)",
        foreground: "var(--color-foreground)",
        primary: "var(--color-primary)",
        accent: "var(--color-accent)",
        card: "var(--color-card)",
        muted: "var(--color-muted)",
        border: "var(--color-border)",
        success: "var(--color-success)",
        warning: "var(--color-warning)"
      },
      borderRadius: {
        DEFAULT: "var(--radius)"
      },
      boxShadow: {
        DEFAULT: "var(--shadow)"
      },
      variables: {
        '--color-background': 'var(--color-background)',
        '--color-foreground': 'var(--color-foreground)',
        '--color-primary': 'var(--color-primary)',
        '--color-accent': 'var(--color-accent)',
        '--color-card': 'var(--color-card)',
        '--color-muted': 'var(--color-muted)',
        '--color-border': 'var(--color-border)',
        '--color-success': 'var(--color-success)',
        '--color-warning': 'var(--color-warning)',
        '--radius': 'var(--radius)',
        '--shadow': 'var(--shadow)'
      }
    }
  },
  plugins: []
};

export default config;