import type { NextConfig } from 'next';
import path from 'path';

const nextConfig: NextConfig = {
  webpack: (config) => {
    // Add alias for @ symbol
    if (!config.resolve.alias) {
      config.resolve.alias = {};
    }
    config.resolve.alias['@'] = path.resolve(__dirname);
    
    // Ensure proper extensions are resolved
    if (!config.resolve.extensions) {
      config.resolve.extensions = [];
    }
    config.resolve.extensions.push('.ts', '.tsx', '.js', '.jsx');
    
    return config;
  },
};

export default nextConfig;
