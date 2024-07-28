<script>
    import { onMount } from 'svelte';
    let processData = {};
  
    async function fetchData() {
      const response = await fetch('http://localhost:5000/data');
      processData = await response.json();
    }
  
    onMount(() => {
      fetchData(); // Initial fetch
      const interval = setInterval(fetchData, 1000); // Fetch data every 1 second
  
      return () => clearInterval(interval); // Clean up interval on component destroy
    });
  </script>
  
  <main>
    <h1>Screen Activity Tracker by Svelte</h1>
    <ul>
      {#each Object.entries(processData) as [key, value]}
        <li>{key}: {value} seconds</li>
      {/each}
    </ul>
  </main>
  