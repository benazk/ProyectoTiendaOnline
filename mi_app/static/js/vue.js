const { createApp } = Vue;

const App = {
  data() {
    return {
        libros : [
            { titulo: "Cien años de soledad", autor: "Gabriel García Márquez", anno: 1967, editorial: "Editorial Sudamericana", img:"imgs/Designer1.png" },
            { titulo: "Don Quijote de la Mancha", autor: "Miguel de Cervantes", anno: 1605, editorial: "Francisco de Robles", img:"imgs/Designer2.png" },
            { titulo: "1984", autor: "George Orwell", anno: 1949, editorial: "Secker & Warburg", img:"imgs/Designer3.png" },
            { titulo: "Matar a un ruiseñor", autor: "Harper Lee", anno: 1960, editorial: "J.B. Lippincott & Co.", img:"imgs/Designer4.png" },
            { titulo: "El gran Gatsby", autor: "F. Scott Fitzgerald", anno: 1925, editorial: "Charles Scribner's Sons", img:"imgs/Designer5.png" },
            { titulo: "La sombra del viento", autor: "Carlos Ruiz Zafón", anno: 2001, editorial: "Planeta", img:"imgs/Designer6.png" },
            { titulo: "Crimen y castigo", autor: "Fiódor Dostoyevski", anno: 1866, editorial: "The Russian Messenger", img:"imgs/Designer7.png" },
            { titulo: "Orgullo y prejuicio", autor: "Jane Austen", anno: 1813, editorial: "T. Egerton, Whitehall", img:"imgs/Designer8.png" },
            { titulo: "El Hobbit", autor: "J.R.R. Tolkien", anno: 1937, editorial: "George Allen & Unwin", img:"imgs/Designer9.png" },
            { titulo: "La casa de los espíritus", autor: "Isabel Allende", anno: 1982, editorial: "Sudamericana", img:"imgs/Designer10.png" },
            { titulo: "El amor en los tiempos del cólera", autor: "Gabriel García Márquez", anno: 1985, editorial: "Editorial Oveja Negra", img:"imgs/Designer1.png" },
            { titulo: "La tregua", autor: "Mario Benedetti", anno: 1960, editorial: "Editorial Siglo XXI", img:"imgs/Designer2.png"},
            { titulo: "El túnel", autor: "Ernesto Sabato", anno: 1948, editorial: "Editorial Sur", img:"imgs/Designer3.png" },
            { titulo: "Los detectives salvajes", autor: "Roberto Bolaño", anno: 1998, editorial: "Anagrama", img:"imgs/Designer4.png" },
            { titulo: "Fahrenheit 451", autor: "Ray Bradbury", anno: 1953, editorial: "Ballantine Books", img:"imgs/Designer5.png" },
            { titulo: "La metamorfosis", autor: "Franz Kafka", anno: 1915, editorial: "Kurt Wolff Verlag", img:"imgs/Designer6.png" },
            { titulo: "Las aventuras de Huckleberry Finn", autor: "Mark Twain", anno: 1884, editorial: "Charles L. Webster And Company", img:"imgs/Designer7.png" },
            { titulo: "Ulises", autor: "James Joyce", anno: 1922, editorial: "Sylvia Beach", img:"imgs/Designer8.png" },
            { titulo: "En busca del tiempo perdido", autor: "Marcel Proust", anno: 1913, editorial: "Grasset", img:"imgs/Designer9.png" },
            { titulo: "El extranjero", autor: "Albert Camus", anno: 1942, editorial: "Gallimard", img:"imgs/Designer10.png" }
          ],
        paginaActual:1,  
        CantLibros:5,

    };
  },
  methods:{

  },
  template: `
    <h1>Lista numerada</h1>
      <table> 
        <tr>
            <td><h3>Título</h3></td>            
            <td><h3>Autor</h3></td>            
            <td><h3>Año</h3></td>                 
            <td><h3>Editorial</h3></td>      
        </tr>
        <tr v-for="libro in libros.slice(CantLibros*(paginaActual-1), CantLibros*paginaActual)">
            <td>{{libro.titulo}}</td>
            <td>{{libro.autor}}</td>
            <td>{{libro.anno}}</td>
            <td>{{libro.editorial}}</td>
        </tr>
    </table>

    <div id="botones">

    <div v-if="paginaActual>1">
        <button v-on:click="paginaActual--">Anterior</button>
    </div>
        {{paginaActual}}
    <div v-if="Math.ceil(libros.length/CantLibros)>paginaActual">
        <button v-on:click="paginaActual++">Siguiente</button>
    </div>

    </div>
  `,
};

//Math.ceil()  redondea numeros con decimales
createApp(App).mount('#app');