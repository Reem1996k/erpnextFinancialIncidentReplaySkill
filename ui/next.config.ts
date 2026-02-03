import type { NextConfig } from 'next';
import path from 'path';

const nextConfig: NextConfig = {
  webpack: (config, { isServer }) => {
    // Add @ alias properly
    if (!config.resolve) {
      config.resolve = {};
    }
    if (!config.resolve.alias) {
      config.resolve.alias = {};
    }
    
    // Set @ to point to the root directory
    config.resolve.alias['@'] = path.resolve(__dirname);
    
    return config;
  },
};

export default nextConfig;
