<script>
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';
  import { invoke } from '@tauri-apps/api/tauri';

  /**
     * @type {Chart<"bar", any[], string> | null}
     */
  let chartInstance = null;
  /**
     * @type {any[]}
     */
  let usageToday = [];
  /**
     * @type {any[]}
     */
  let mostUsedApps = [];
  let totalUsage = "0 Hour 0 Minutes";

  async function fetchData() {
    try {
      const data = await invoke('get_app_usage_data');
      updateDashboard(data);
    } catch (error) {
      console.error('Failed to fetch data:', error);
    }
  }

  /**
     * @param {{ hourly_usage: any[]; most_used_apps: any[]; total_usage: any; }} data
     */
  function updateDashboard(data) {
    usageToday = data.hourly_usage;
    mostUsedApps = data.most_used_apps;
    totalUsage = formatDuration(data.total_usage);
    updateChart();
  }

  function updateChart() {
    if (chartInstance) {
      chartInstance.data.datasets[0].data = usageToday;
      chartInstance.update();
    }
  }

  /**
     * @param {number} minutes
     */
  function formatDuration(minutes) {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours} Hour${hours !== 1 ? 's' : ''} ${mins} Minute${mins !== 1 ? 's' : ''}`;
  }

  onMount(() => {
    const ctx = document.querySelector('#usageChart') as HTMLCanvasElement;
    if (ctx) {
      chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: Array.from({length: 24}, (_, i) => i.toString().padStart(2, '0')),
          datasets: [{
            label: 'Usage (minutes)',
            data: usageToday,
            backgroundColor: 'rgba(54, 162, 235, 0.5)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              max: 60,
              ticks: {
                stepSize: 20
              }
            }
          }
        }
      });

      fetchData();
      const interval = setInterval(fetchData, 60000); // Update every minute
      return () => clearInterval(interval);
    }
  });
</script>

<div class="bg-gray-900 text-white p-6">
  <h1 class="text-2xl font-bold mb-4">App Tracker Dashboard</h1>
  
  <div class="mb-6">
    <h2 class="text-xl mb-2">Today's Usage: {totalUsage}</h2>
    <canvas id="usageChart" width="400" height="200"></canvas>
  </div>
  
  <div>
    <h2 class="text-xl mb-2">Most Used Apps Today</h2>
    <ul>
      {#each mostUsedApps as app}
        <li class="mb-2">
          <span class="font-semibold">{app.name}</span>: {formatDuration(app.duration)}
        </li>
      {/each}
    </ul>
  </div>
</div>
