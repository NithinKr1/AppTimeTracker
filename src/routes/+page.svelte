<script>
    import { onMount } from 'svelte';
    import { invoke } from '@tauri-apps/api/tauri';

    let processData = {};
    let checked = false;
    let serverStartTime = '';
  
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

    async function handleChange() {
        checked = !checked;
        await invoke('toggle_startup', { enable: checked });
    }
  
    onMount(() => {
        serverStartTime = new Date().toLocaleString();
        fetchData();
        const interval = setInterval(fetchData, 1000);
  
        return () => clearInterval(interval);
    });
</script>
  
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
        display: flex;
        justify-content: space-between;
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

    /* The switch - the box around the slider */
    .switch {
        position: relative;
        display: inline-block;
        width: 60px;
        height: 34px;
    }

    /* Hide default HTML checkbox */
    .switch input {
        opacity: 0;
        width: 0;
        height: 0;
    }

    /* The slider */
    .slider {
        position: absolute;
        cursor: pointer;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: #ccc;
        -webkit-transition: .4s;
        transition: .4s;
    }

    .slider:before {
        position: absolute;
        content: "";
        height: 26px;
        width: 26px;
        left: 4px;
        bottom: 4px;
        background-color: white;
        -webkit-transition: .4s;
        transition: .4s;
    }

    input:checked + .slider {
        background-color: #2196F3;
    }

    input:focus + .slider {
        box-shadow: 0 0 1px #2196F3;
    }

    input:checked + .slider:before {
        -webkit-transform: translateX(26px);
        -ms-transform: translateX(26px);
        transform: translateX(26px);
    }

    /* Rounded sliders */
    .slider.round {
        border-radius: 34px;
    }

    .slider.round:before {
        border-radius: 50%;
    } 

    .switch-description {
        margin-right: 12px;
    }
</style>
  
<main>
    <h1>
        <span>Most used App Today</span>
        <span>App opened at {serverStartTime}</span>
    </h1>
    <div>
        <span class="switch-description">Enable app on Startup</span>
        <label class="switch">
            <input type="checkbox" bind:checked={checked} on:change={handleChange}>
            <span class="slider round"></span>
        </label>
    </div>
    <ul>
        {#each Object.entries(processData).sort((a, b) => b[1] - a[1]) as [key, value]}
            <li>
                <span>{key}</span>
                <span>{formatTime(value)}</span>
            </li>
        {/each}
    </ul>
</main>
