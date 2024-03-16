<!-- App.svelte -->
<!--npm install --save svelte-routing-->
<script>
	import { Router, Route, Link } from 'svelte-routing';
  import First from './components/First.svelte';
  import Log from './components/Log.svelte';
  
  import Question1 from './components/Question1.svelte';// Importa tu componente Question1
  import Question2 from './components/Question2.svelte';// Importa tu componente Question2

  import Results from './components/Results.svelte'; // user's results (with AI)

</script>




<Router>

	<Route path="/">
		<Log></Log>
	</Route>


	<Route path="/register_0">
		<Question1></Question1>
	</Route>

	<Route path="/register_50">
		<Question2></Question2>
	</Route>


	<Route path="/results">
		<Results></Results>
	</Route>

	
  </Router>

<!--
<div>
	
	<Log />	
  
</div>
-->



<style>
  /* Estilos para App.svelte */
</style>
