/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['images.unsplash.com', 'via.placeholder.com'],
    unoptimized: true
  },
  eslint: {
    ignoreDuringBuilds: true
  },
  typescript: {
    ignoreBuildErrors: true
  },
  async rewrites() {
    return [
      {
        source: '/api/chat/stream',
        destination: process.env.NODE_ENV === 'production' 
          ? 'https://phoree-chatbot-api.onrender.com/api/chat/stream'
          : 'http://localhost:10000/api/chat/stream'
      }
    ]
  }
}

module.exports = nextConfig 