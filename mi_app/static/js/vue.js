const { createApp } = Vue;

const productos = Vue.createApp({
  template: `
    <div v-if="!unprod">
      <h1>Lista de Productos</h1>
      <ul>
        
        <li v-for="(item, index) in productos">
          <a :href="'/producto/' + index">{{ item.nombre }}</a><span>Categoría: {{ item.categoria }}</span>
        </li>
      </ul>
    </div>

    <div v-if="unprod">
      <h1>{{ productoSeleccionado.nombre }}</h1>
      <p>Categoría: {{ productoSeleccionado.categoria }}</p>
      <p>{{ productoSeleccionado.descripcion }}</p>
      <a href="/">Volver a la lista</a>
    </div>

  `,
  beforeMount() {
    this.cargarProductos()
    this.cargarCategorias()
  },
  data() {
    return {
        productos: [],
        categorias: [],
        productoSeleccionado: {},
        unprod: false
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
      
    },
    async cargarCategorias() {
      try {
        const response = await fetch('/api/categorias');
        this.categorias = await response.json();
      } catch (error) {
        console.error("Error cargando JSON:", error);
      }
      
    },

    async cargarProducto(id) {
      try {
        const response = await fetch(`/producto/${id}`);
        this.productoSeleccionado = await response.json();
        this.unprod = true
      } catch (error) {
        console.error("Error obteniendo el producto:", error);
      }
    },
    mostrarProductosTodos(){
        console.log(typeof(this.productos))
    }
  },
  
});
productos.mount('#app')

