const { createApp } = Vue;

const productos = Vue.createApp({
  delimiters: ['[[', ']]'],
  template: `
    <ul>
      <li v-for="prod in carrito">
        Usuario: [[prod.nombreUsuario]]
        Producto: [[prod.nombre]]
        Hora: [[prod.hora]]
        <a :href="flaskUrls.productDetail + prod.idUsuario + '/' + prod.id"><button>Eliminar producto</button></a>
      </li>
    </ul>
    
  `,
  beforeMount() {
    this.cargarCarrito()
    
  },
  data() {
    return {
      carrito: {},
      flaskUrls: window.flaskUrls
    };

  },
  methods: {
    async cargarCarrito() {
      try {
        const response = await fetch(`/getcarrito/benat`);
        this.carrito = await response.json();
        
      } catch (error) {
        console.error("Error obteniendo el producto:", error);
      }
      console.log("ola gente")
    },
  },
  
});
productos.mount('#app')

