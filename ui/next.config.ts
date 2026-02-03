import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Allow ngrok origin for development
  allowedDevOrigins: [
    'lichenlike-kellee-autocratically.ngrok-free.dev',
  ],
  // Turbopack config for path alias (Next.js 16 default bundler)
  turbopack: {
    resolveAlias: {
      '@': './',
    },
  },
};

export default nextConfig;
