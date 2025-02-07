const { createApp } = Vue;

const productos = Vue.createApp({
  delimiters: ['[[', ']]'],
  template: `
    <!-- Contenedor principal 2 columnas-->
    <div class="container mb-4 mt-3">
        <h1 class="text-light text-center mt-3">Carrito</h1>
        <div class="row">
            <div class="col-sm-12 col-md-6 col-lg-8">
                <!-- Contenedor producto del carrito-->
                <div class="container" v-for="prod in carrito">
                    <div class="row azul" style="padding: 20px;">
                        <!-- Contenedor imagen-->
                        <div class="col-sm-12 col-md-6 col-lg-8">
                            <div class="container" id="imagen">
                                <img :src="flaskUrls.image + prod.imagen"
                                    class="img-fluid mx-auto d-block" alt="Ejemplo de imagen responsiva">
                            </div>
                        </div>
                        <!-- Contenedor detalles de producto-->
                        <div class="col-sm-12 col-md-6 col-lg-4">
                            <div class="container">
                                <div class="row">
                                    <h4 class="text-light">[[prod.nombre]]</h4>
                                    <p class="text-success">[[prod.precio]] €</p>
                                </div>
                                <a :href="flaskUrls.productDetail + prod.idUsuario + '/' + prod.id">
                                <button type="button" class="btn btn-danger btn-sm" @click="calcularTotal">Eliminar producto</button>
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
                            <h3 class="text-light">Total estimado:</h3>
                            <p class="text-success">[[precioTotal]]€</p>
                            <p class="text-light">Los impuestos de venta se calcularán durante el pago (si es aplicable)</p>
                        </div>
                    </div>
                    <a :href="flaskUrls.pago"><button type="button" class="btn btn-primary btn-sm text-light">Continuar con el pago</button><br></a>
                    <button type="button" class="btn btn- btn-sm text-light"><a :href="flaskUrls.seguirComprando" style="text-decoration: none; color: inherit;">Seguir comprando</a></button>
                </div>
                <div class="container text-light" id="acuerdo_suscriptor">
                    La compra de un producto digital otorga una licencia para el producto en UnderKeys.
                    Para ver los términos y condiciones completos, consulta el <strong>Acuerdo de Suscriptor a
                        UnderKeys.</strong>
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
        for (prod of this.carrito) {
          this.precioTotal += Number(prod.precio)
        }
      } catch (error) {
        console.error("Error obteniendo el producto:", error);
      }
    },
    calcularTotal() {
      for (prod of this.carrito) {
        this.precioTotal += Number(prod.precio)
      }
    },
    conver(tipo) {
      fetch(' https://v6.exchangerate-api.com/v6/2d32faab06a3c28f785d7e33/latest/EUR')
        .then(response => response.json()) //Cuando se conecte lo anterior y da una respuesta ok el servidor, que haga lo siguiente
        .then(data => {

          for (x in data.conversion_rates) {
            if (tipo == x) {
              this.tipoMoneda = tipo;
              this.cambio = data.conversion_rates[x]
              document.getElementById("monedaTitulo").innerHTML = tipo

              if (tipo == "EUR") {
                this.Simbolo = "€"
              } else if (tipo == "USD") {
                this.Simbolo = "$"
              } else if (tipo == "NIO") {
                this.Simbolo = "C$"
              } else if (tipo == "JPY") {
                this.Simbolo = "¥"
              }
            }
          }
        })     //Exchange Rate API
    },

  },

});
productos.mount('#app')

