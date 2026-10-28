// Vite configuration for the frontend service.
// Add aliases, proxy settings, or deployment-specific options here.
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
});
