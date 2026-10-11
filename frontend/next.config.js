/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async redirects() {
    return [
      {
        source: '/audit',
        destination: '/',
        permanent: false,
      },
      {
        source: '/contracts/:path*',
        destination: '/',
        permanent: false,
      },
    ];
  },
  async rewrites() {
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';
    return [
      {
        source: '/api/v1/:path*',
        destination: `${backendUrl}/api/v1/:path*`,
      },
      {
        source: '/health',
        destination: `${backendUrl}/health`,
      },
      {
        source: '/mcp/:path*',
        destination: `${backendUrl}/mcp/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
