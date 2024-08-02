<style>
  main {
      background-color: #242424;
      color: #ffffff;
      font-family: 'Segoe UI', sans-serif;
      padding: 1em;
  }

  h1 {
      font-size: 1.5em;
      margin-bottom: 1em;
  }

  ul {
      list-style-type: none;
      padding: 0;
  }

  li {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #444;
      padding: 0.5em 0;
  }

  li:last-child {
      border-bottom: none;
  }
</style>

<script>
  import { onMount } from 'svelte';
  let processData = {};

  async function fetchData() {
      const response = await fetch('http://localhost:5000/data');
      processData = await response.json();
  }

  function formatTime(seconds) {
      const hrs = Math.floor(seconds / 3600);
      const mins = Math.floor((seconds % 3600) / 60);
      const secs = seconds % 60;
      return `${hrs} hour ${mins} min ${secs} sec`;
  }

  onMount(() => {
      fetchData(); // Initial fetch
      const interval = setInterval(fetchData, 1000); // Fetch data every 1 second

      return () => clearInterval(interval); // Clean up interval on component destroy
  });
</script>

<main>
  <h1>Most used App Today</h1>
  <ul>
      {#each Object.entries(processData).sort((a, b) => b[1] - a[1]) as [key, value]}
          <li>
              <span>{key}</span>
              <span>{formatTime(value)}</span>
          </li>
      {/each}
  </ul>
</main>