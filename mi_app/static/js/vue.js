const { createApp } = Vue;

const productos = Vue.createApp({
  delimiters: ['[[', ']]'],
  template: `
    <!-- Contenedor principal 2 columnas-->
    <div class="container">
        <h1>Carrito</h1>
        <div class="row">
            <div class="col-sm-12 col-md-6 col-lg-7 me-2 azul ">
                <!-- Contenedor producto del carrito-->
                <div class="container" style="padding: 20px;" v-for="prod in carrito">
                    <div class="row">
                        <!-- Contenedor imagen-->
                        <div class="col-sm-12 col-md-6 col-lg-8 ">
                            <div class="container" id="imagen">
                                <img :src="flaskUrls.image + prod.imagen"
                                    class="img-fluid mx-auto d-block" alt="Ejemplo de imagen responsiva">
                            </div>
                        </div>
                        <!-- Contenedor detalles de producto-->
                        <div class="col-sm-12 col-md-6 col-lg-4">
                            <div class="container">
                                <div class="row">
                                    <p>[[prod.nombre]]</p>
                                    <p>[[prod.precio]] €</p>
                                </div>
                                <button type="button" class="btn btn-secondary btn-sm"> Pagar</button>
                                <a :href="flaskUrls.productDetail + prod.idUsuario + '/' + prod.id">
                                <button type="button" class="btn btn-secondary btn-sm" @click="calcularTotal">Eliminar producto</button>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-sm-12 col-md-6 col-lg-4 azul">
                <div class="container" style="padding: 20px;">
                    <div class="row">
                        <div class="container" id="datos">
                            <h3>Total estimado:</h3>
                            <p>[[precioTotal]]€</p>
                            <p>Los impuestos de venta se calcularán durante el pago (si es aplicable)</p>
                        </div>
                    </div>
                    <button type="button" class="btn btn-secondary btn-sm">Continuar con el pago</button><br>
                    <button type="button" class="btn btn- btn-sm">Seguir comprando</button>
                    <button type="button"class="btn btn- btn-sm">Eliminar todos los articulos</button>
                </div>
                <div class="container" id="imagen2">
                    La compra de un producto digital otorga una licencia para el producto en Steam.
                    Para ver los términos y condiciones completos, consulta el <strong>Acuerdo de Suscriptor a
                        Steam.</strong>
                </div>
            </div>
        </div>
    </div>
    
  `,
  beforeMount() {
    this.cargarCarrito()
  },
  data() {
    return {
      carrito: {},
      flaskUrls: window.flaskUrls,
      precioTotal: 0
    };

  },
  methods: {
    async cargarCarrito() {
      try {
        const response = await fetch(`/getcarrito/benat`);
        this.carrito = await response.json();
        for(prod of this.carrito){
          this.precioTotal += Number(prod.precio)
        }
      } catch (error) {
        console.error("Error obteniendo el producto:", error);
      }
    },
    calcularTotal(){
      for(prod of this.carrito){
        this.precioTotal += Number(prod.precio)
      }
    }
  },
  
});
productos.mount('#app')

