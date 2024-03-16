<script>
    import { navigate } from 'svelte-routing';
    export let option = 'none';
    function login(){
        option = 'login';
        console.log(option);
        navigate("/login")
    }

    function register(){
        option = 'register';
        console.log(option);
        navigate("/register_0")
    }
</script>

<video id="videoBackground" autoplay loop muted playsinline>
    <source src="vecteezy_abstract-blue-swirls-in-motion-looping_22919364.mp4" type="video/mp4">
    <!-- Añade aquí más etiquetas source para otros formatos de video como webm, ogg, etc. -->
    Tu navegador no soporta el elemento de video.
</video>

<div class="content">
    <div class="navbar">
        <h1 id="containerParent">MiChamba</h1>
        <img id="containerLog" class="logo" src="LogoMiChamba.png" alt="Imagen">
    </div>

    <button class="button1" on:click={register}>Register</button>
    <button class="button2" on:click={login}>Login</button>
</div>



<style>
body {
    margin: 0;
    overflow: hidden; /* Ocultar barras de desplazamiento */
}

#videoBackground {
    position: fixed;
    top: 0;
    left: 0;
    min-width: 60%;
    min-height: 60%;
    z-index: -1; /* Colocar el video detrás de otros elementos */
}

.content {
    position: relative; /* Asegurar que el contenido aparezca encima del video */
    z-index: 1; /* Colocar el contenido encima del video */
}

.navbar {
    background-color: rgba(0, 0, 0, 0.5); /* Fondo semi-transparente para la barra superior */
    padding: 10px;
    text-align: center;
}

#containerParent {
    color: white;
    font-size: 50px;
}

#containerLog {
    max-width: 100px;
    max-height: 100px;
    position: absolute;
    top: 30%;
    left: 50%;
    transform: translate(-50%, -50%);
}


  .button1,
  .button2 {
    background-color: #7c7070ce; /* Cambiar a color negro sólido */
    border: none;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 20px;
    margin: 280px 10px; /* Ajusta el espacio entre los botones y el margen superior */
    margin-left: 390px; /* Centrar horizontalmente */
    margin-right: 10px; /* Centrar horizontalmente */
  }
</style>

