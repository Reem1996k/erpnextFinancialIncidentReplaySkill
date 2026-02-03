import type { NextConfig } from "next";
import path from "path";

const nextConfig: NextConfig = {
  // Explicit webpack config for path alias
  webpack: (config) => {
    config.resolve = config.resolve || {};
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': path.resolve(__dirname),
    };
    return config;
  },
};

export default nextConfig;
