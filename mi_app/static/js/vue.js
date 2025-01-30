const { createApp } = Vue;

const productos = Vue.createApp({
  template: `
    <div>
      <h1>Lista de Productos</h1>
      <ul>
        
        <li v-for="(item, index) in productos">
          <a :href="'/producto/' + index">{{ item.nombre }}</a><span>Categoría: {{ item.categoria }}</span>
        </li>
      </ul>
    </div>

  `,
  beforeMount() {
    this.cargarProductos()
  },
  data() {
    return {
        productos: [],
    };
  },
  methods: {
    async cargarProductos() {
      const now = new Date();
      this.unprod = false
      try {
        const response = await fetch('/api/productos');
        this.productos = await response.json();
        console.log("milisegundos ahora: " + now.getMilliseconds())
        console.log(this.productos)
      } catch (error) {
        console.error("Error cargando JSON:", error);
      }
      
    }
  },
  
});
productos.mount('#app')

