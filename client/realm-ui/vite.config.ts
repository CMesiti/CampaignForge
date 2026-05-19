import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // Proxy API calls to Flask in dev so you don't need CORS config
      "/auth": "http://localhost:5000",
      "/v1": "http://localhost:5000",
      "/agent": "http://localhost:5000",
    },
  },
});
