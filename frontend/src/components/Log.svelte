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




<div class="all">
    <h1 id="containerParent">MiChamba</h1>
    <img id="containerLog" class="logo" src="loading.png" alt="Imagen">
</div>

<button class="button1" on:click={register}>Register</button>
<button class="button2" on:click={login}>Login</button>

<!--
<div class="button1" onclick="window.location='/register'">Register</div>
<button class="button2" onclick="window.location='/login'">Login</button>
-->

<style>


.all{
    background-color: rgb (255, 122 89) ;
}

#containerParent{
    color:red;
    text-align: center;
    left:50%;
    transform: translate(0%,150%);
    font-size: 40px;
}


#containerLog{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}


.button1 {
    background-color: #04AA6D;
    border: none;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    position: absolute;
    top: 80%;
    left:40%;
}

.button2 {
  background-color: #04AA6D; /* Green */
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  position: absolute;
  top: 80%;
  right:40%;
}



</style>