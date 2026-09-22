import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://www.fishka.spb.ru",
  base: "/new",
  trailingSlash: "never",
  build: {
    format: "directory",
  },
});
