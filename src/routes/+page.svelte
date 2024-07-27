<script>
    import { onMount } from 'svelte';
    let processData = {};
  
    async function fetchData() {
      const response = await fetch('http://localhost:5000/data');
      processData = await response.json();
    }
  
    onMount(fetchData);
  </script>
  
  <main>
    <h1>Screen Activity Tracker</h1>
    <ul>
      {#each Object.entries(processData) as [key, value]}
        <li>{key}: {value} seconds</li>
      {/each}
    </ul>
  </main>
  