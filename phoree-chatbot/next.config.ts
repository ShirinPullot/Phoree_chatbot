const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/chat/stream',
        destination: '/api/chat'
      }
    ]
  }
}

module.exports = nextConfig

