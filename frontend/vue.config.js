module.exports = {
  devServer: {
    port: 3000,
    proxy: {
      '/api': {
        target:'https://diary-generator-backend.onrender.com',       //http://localhost:5000',
        changeOrigin: true
      }
    }
  }
}
