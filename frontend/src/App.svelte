<!-- App.svelte -->
<script>
  import First from './components/First.svelte';
  import Log,{option} from './components/Log.svelte';
  
  console.log(option);
</script>

<div>
	
	{#if option === 'none'}
		<Log />	
	{:else}
		<p>HEllo</p>
	{/if}
  
</div>

<style>
  /* Estilos para App.svelte */
</style>
