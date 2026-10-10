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
    ]
  },
  async rewrites() {
    return [
      {
        source: '/api/v1/:path*',
        destination: process.env.BACKEND_URL 
          ? `${process.env.BACKEND_URL}/api/v1/:path*` 
          : (process.env.NEXT_PUBLIC_API_URL 
            ? `${process.env.NEXT_PUBLIC_API_URL}/api/v1/:path*` 
            : 'http://localhost:8000/api/v1/:path*'),
      },
      {
        source: '/mcp/:path*',
        destination: process.env.BACKEND_URL 
          ? `${process.env.BACKEND_URL}/mcp/:path*` 
          : (process.env.NEXT_PUBLIC_API_URL 
            ? `${process.env.NEXT_PUBLIC_API_URL}/mcp/:path*` 
            : 'http://localhost:8000/mcp/:path*'),
      },
    ]
  },
}

module.exports = nextConfig

