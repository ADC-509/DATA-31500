<script>
  import { onMount } from 'svelte';
  import Scatter from './Scatter.svelte';
  import * as d3 from 'd3';
  import * as XLSX from 'xlsx';

  const diseases = [
    { label: 'Diabetes', code: 'DIABDX_M18' },
    { label: 'Asthma', code: 'ASTHDX' },
    { label: 'ADHD', code: 'ADHDADDX' }
  ];

  let selectedDisease = diseases[0];
  let data = [];
  const loadDataForDisease = async () => {
    try {
      // Load the CSV file
      const rawData = await d3.csv('health_data.csv'); 

      // Filter data for the selected disease
      data = rawData
        .filter(d => d[selectedDisease.code] === '1') // Filter by disease indicator
        .map(d => ({
          income: +d.FAMINC22, // Convert to numbers
          expenditure: +d.TOTEXP22 // Convert to numbers
        }))
        .filter(d => d.income != null && d.expenditure != null); // Remove incomplete data

      console.log("Filtered data:", data);
    } catch (error) {
      console.error('Error loading data:', error);
    }
  };

  onMount(() => {
    loadDataForDisease();
  });

  $: if (selectedDisease) {
    loadDataForDisease();
  }
</script>

<div class="container">
  <div class="title">The Cost of Chronic Conditions: A Look at Healthcare Spending and Access in the U.S.</div>
  <div class="subtitle">An Interactive Data Story</div>

  <div class="introduction">
    <p>In the United States, managing chronic health conditions is not just a matter of medical concern; it also comes with significant financial challenges. But not everyone faces these costs equally. How does healthcare spending vary based on income, especially for people with chronic conditions?</p>
    
    <p>In this interactive article, we explore the economic burden of chronic conditions such as diabetes and hypertension across different income groups and highlight the disparities in healthcare access and spending. Use the visualizations and interactive tools throughout this article to gain insights into these pressing issues and see how factors like income and age can affect healthcare costs and utilization.</p>
  </div>

  <div class="section">
    <div class="section-title">1. Disease Recognition</div>
    <p>Select a chronic condition to view healthcare expenditures and utilization patterns:</p>
    
    <div class="dropdown">
      <label for="disease-select">Choose a disease:</label>
      <select id="disease-select" bind:value={selectedDisease} on:change={loadDataForDisease}>
        {#each diseases as disease}
          <option value={disease}>{disease.label}</option>
        {/each}
      </select>
    </div>

    {#if data.length > 0}
      <Scatter {data} disease={selectedDisease} />
    {:else}
      <div class="visualization-placeholder">
        <p>Loading data for {selectedDisease.label}...</p>
      </div>
    {/if}

  </div>

</div>

<style>
  /* Base container styling */
  .container {
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }

  /* Light mode styling */
  :root {
    --background-color: #ffffff;
    --text-color: #333;
    --title-color: #333;
    --subtitle-color: #666;
  }

  /* Dark mode styling */
  @media (prefers-color-scheme: dark) {
    :root {
      --background-color: #121212;
      --text-color: #e0e0e0;
      --title-color: #ffffff;
      --subtitle-color: #bbbbbb;
    }
  }

  /* Apply adaptive colors */
  body {
    background-color: var(--background-color);
    color: var(--text-color);
  }

  .title {
    font-size: 2em;
    font-weight: bold;
    text-align: center;
    color: var(--title-color);
    margin-bottom: 20px;
  }

  .subtitle {
    font-size: 1.2em;
    color: var(--subtitle-color);
    text-align: center;
    margin-bottom: 20px;
  }

  .introduction {
    font-size: 1em;
    line-height: 1.6;
    color: var(--text-color);
    text-align: justify;
  }

  .section-title {
    font-size: 1.5em;
    font-weight: bold;
    color: var(--title-color);
    margin-bottom: 15px;
  }

  .dropdown {
    margin-bottom: 20px;
  }

  .visualization-placeholder {
    font-size: 1em;
    color: var(--text-color);
  }

  /* Styling for responsive design */
  @media (max-width: 600px) {
    .title {
      font-size: 1.5em;
    }

    .subtitle {
      font-size: 1em;
    }

    .introduction {
      font-size: 0.9em;
    }

    .section-title {
      font-size: 1.2em;
    }

    .visualization-placeholder {
      font-size: 0.9em;
    }
  }
</style>