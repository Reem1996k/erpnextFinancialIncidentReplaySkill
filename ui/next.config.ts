import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Turbopack config for path alias (Next.js 16 default bundler)
  turbopack: {
    resolveAlias: {
      '@': './',
    },
  },
};

export default nextConfig;
