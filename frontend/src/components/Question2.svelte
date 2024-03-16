
<script>

    import { navigate } from 'svelte-routing';

    function finish(){
        navigate("/results")
    }
</script>

<div class = "question">
    <h1>Pregunta 11</h1>
</div>
  


<button class="button" on:click={finish}>Finish</button>



<style>

.button{
    background-color: #4659cd;
    border: none;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    position: absolute;
    top: 80%;
    left:90%;
}

</style>