<script>
  import { onMount } from 'svelte';
  import Scatter from './Scatter.svelte';
  import Histogram from './Histogram.svelte';
  import BarChart from './BarChart.svelte';
  import * as d3 from 'd3';

  const diseases = [
    { label: 'Diabetes', code: 'DIABDX_M18' },
    { label: 'Asthma', code: 'ASTHDX' },
    { label: 'ADHD', code: 'ADHDADDX' }
  ];

  let selectedDisease = diseases[0];
  let selectedAgeGroup = 'All';
  let ageGroups = ['All', '0-17', '18-44', '45-64', '65+'];
  let data = [];
  let visitsData = [];
  let showScatter = true;

  // Variables to store disease counts, average income, and expenditure
  let diseaseCounts = { DIABDX_M18: 0, ASTHDX: 0, ADHDADDX: 0 };
  let avgIncome = 0;
  let avgExpenditure = 0;

  // Variables for user input in prediction
  let userInputs = {
    DIABDX_M18: 0,
    ADHDADDX: 0,
    ASTHDX: 0,
    FAMINC22: 0,
    OBTOTV22: 0,
    AGE22X: 0
  };
  let predictedTOTEXP22 = null;

  // Function to load data for Disease Recognition section and calculate totals and averages
  const loadDataForDisease = async () => {
    try {
      const rawData = await d3.csv('health_data.csv');
      
      // Calculate disease totals
      diseaseCounts = {
        DIABDX_M18: rawData.filter(d => d.DIABDX_M18 === '1').length,
        ASTHDX: rawData.filter(d => d.ASTHDX === '1').length,
        ADHDADDX: rawData.filter(d => d.ADHDADDX === '1').length
      };

      // Filter and process data based on selected disease
      data = rawData
        .filter(d => d[selectedDisease.code] === '1')
        .map(d => ({
          income: +d.FAMINC22,
          expenditure: +d.TOTEXP22,
          visits: +d.OBTOTV22,
          age: +d.AGE22X
        }))
        .filter(d => d.income && d.expenditure && d.visits && d.age);
      
      // Calculate average income and expenditure for the selected disease
      avgIncome = d3.mean(data, d => d.income);
      avgExpenditure = d3.mean(data, d => d.expenditure);
    } catch (error) {
      console.error('Error loading data:', error);
    }
  };

  // Function to load data for visits (for the Bar Chart)
  const loadVisitsData = async () => {
    visitsData = data
      .filter(d => selectedAgeGroup === 'All' || categorizeAgeGroup(d.age) === selectedAgeGroup)
      .map(d => ({
        income: d.income,
        visits: d.visits
      }));
  };

  // Helper function to categorize age into groups
  function categorizeAgeGroup(age) {
    if (age < 18) return '0-17';
    if (age < 45) return '18-44';
    if (age < 65) return '45-64';
    return '65+';
  }

  // Functions to toggle scatter/histogram views
  function animateToHistogram() {
    showScatter = false;
  }
  function animateToScatter() {
    showScatter = true;
  }

  onMount(() => {
    loadDataForDisease();
    loadVisitsData();
  });

  $: if (selectedDisease) {
    loadDataForDisease();
  }

  $: if (selectedAgeGroup) {
    loadVisitsData();
  }

  // Linear model coefficients from R
  const coefficients = {
    intercept: 4278.403724,
    DIABDX_M18: -2183.849586,
    ADHDADDX: -22.857638,
    ASTHDX: 266.926943,
    FAMINC22: -0.004642,
    OBTOTV22: 526.270392,
    AGE22X: 88.744245
  };

  // Function to calculate prediction using the linear model
  function getPrediction() {
    predictedTOTEXP22 = coefficients.intercept
      + coefficients.DIABDX_M18 * userInputs.DIABDX_M18
      + coefficients.ADHDADDX * userInputs.ADHDADDX
      + coefficients.ASTHDX * userInputs.ASTHDX
      + coefficients.FAMINC22 * userInputs.FAMINC22
      + coefficients.OBTOTV22 * userInputs.OBTOTV22
      + coefficients.AGE22X * userInputs.AGE22X;
  }

  // Prediction function to call XGBoost API
  // async function getPrediction() {
  //   try {
  //     const response = await fetch('http://127.0.0.1:5000/predict', {
  //       method: 'POST',
  //       headers: {
  //         'Content-Type': 'application/json'
  //       },
  //       body: JSON.stringify(userInputs)
  //     });
  //     const data = await response.json();
  //     predictedTOTEXP22 = data.TOTEXP22_prediction;
  //   } catch (error) {
  //     console.error("Error fetching prediction:", error);
  //   }
  // }
</script>

<div class="container">
  <div class="title">The Cost of Chronic Conditions: A Look at Healthcare Spending and Access in the U.S.</div>
  <div class="subtitle">An Interactive Data Story</div>

  <!-- Introduction Section -->
  <div class="introduction">
    <p>In the United States, managing chronic health conditions is not just a matter of medical concern; it also comes with significant financial challenges. But not everyone faces these costs equally. How does healthcare spending vary based on income, especially for people with chronic conditions?</p>
    <p>In this interactive article, we explore the economic burden of chronic conditions across different income groups and highlight the disparities in healthcare access and spending.</p>
  </div>

  <!-- Section 1: Disease Recognition -->
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
      {#if showScatter}
        <Scatter {data} disease={selectedDisease} />
      {:else}
        <Histogram {data} disease={selectedDisease} />
      {/if}
    {:else}
      <div class="visualization-placeholder">
        <p>Loading data for {selectedDisease.label}...</p>
      </div>
    {/if}

    <div class="buttons">
      <button on:click={animateToHistogram}>Animate to Histogram</button>
      <button on:click={animateToScatter}>Reset to Scatter Plot</button>
    </div>

    <!-- Data Story Narrative -->
    <p>
      Notice how healthcare expenditures cluster among lower-income groups with distinct patterns for each condition. Use the zoom feature in the scatter plot to explore these clusters more closely. Are there surprises as you zoom in on specific data points?
    </p>
    
    <p>
      The scatter plot below shows how healthcare expenditures differ based on income for 
      <span class="disease-link" title={`Total cases: ${diseaseCounts[selectedDisease.code]}`}>
        <a href={`https://en.wikipedia.org/wiki/${selectedDisease.label}`} 
           target="_blank" 
           rel="noopener noreferrer">
          {selectedDisease.label}
        </a>
      </span>.
      For {selectedDisease.label}, the average income level among individuals is  ${avgIncome.toFixed(2)} and the average healthcare expenditure is ${avgExpenditure.toFixed(2)}.
      When switching to the histogram view, a pattern often emerges: expenditures are mostly lower, but a small group faces much higher costs.
    </p>
    
    {#if selectedDisease.code === 'ASTHDX'}
      <p>
        For asthma, costs vary significantly, reflecting diverse treatment needs. Try zooming in to observe this variability more closely, especially at different income levels.
      </p>
    {:else if selectedDisease.code === 'ADHDADDX'}
      <p>
        For ADHD, expenditures tend to be more concentrated on the lower end, likely due to more standardized treatment requirements. Zoom in to see how spending clusters by income.
      </p>
    {:else if selectedDisease.code === 'DIABDX_M18'}
      <p>
        For diabetes, costs can increase with complications, which may lead to higher spending in some income groups. Use the zoom function to get a detailed view of these high-spending cases among lower-income individuals.
      </p>
    {:else}
      <p>
        Each condition has its unique pattern in healthcare spending, reflecting different treatment needs and costs. Zoom in on the scatter plot to explore these differences for the selected condition in detail.
      </p>
    {/if}
    
    <p>
      These insights underscore the varying financial burdens of chronic conditions, particularly on vulnerable groups. Through this visualization, you can explore where financial support may be most needed.
    </p>
  </div>

  <!-- Section 2: Unequal Access to Healthcare -->
  <div class="section">
    <div class="section-title">2. Unequal Access to Healthcare</div>
    <p>
      Beyond just costs, access to healthcare services like regular check-ups and specialist visits is essential for managing chronic conditions effectively. But do people across income levels with 
      <a href={`https://en.wikipedia.org/wiki/${selectedDisease.label}`} target="_blank" rel="noopener noreferrer">
        {selectedDisease.label}
      </a>
      have similar access to these services? Let’s explore the frequency of medical visits for individuals with 
      <a href={`https://en.wikipedia.org/wiki/${selectedDisease.label}`} target="_blank" rel="noopener noreferrer">
        {selectedDisease.label}
      </a>
      and compare it to their income.
    </p>
        
    <div class="dropdown">
      <label for="age-group-select">Filter by Age Group:</label>
      <select id="age-group-select" bind:value={selectedAgeGroup} on:change={loadVisitsData}>
        {#each ageGroups as ageGroup}
          <option value={ageGroup}>{ageGroup}</option>
        {/each}
      </select>
    </div>

    <BarChart {visitsData} condition={selectedDisease} />

    <p>Filter by age group and condition to see the variations in healthcare utilization. Are certain age groups less likely to visit their healthcare providers? What differences can you observe when switching between conditions?</p>

    <!-- Narrative and Analysis -->
    <p>This chart is ordered by income levels, helping to illustrate which income groups have more frequent healthcare visits. Higher-income individuals may access healthcare differently than lower-income groups, providing insights into access disparities.</p>
    
    <p>When ordered by income, we observe that higher-income groups generally have more regular healthcare visits, particularly among older age groups. This pattern indicates better healthcare access among wealthier individuals, possibly due to affordability and proximity to healthcare services.</p>

    <p>For younger age groups, however, the distribution of visits is more varied, suggesting that income may play a smaller role in healthcare access for younger populations. This trend might be due to various factors, such as employer-sponsored healthcare or lower healthcare needs among younger people.</p>

    <p>Switching the chart to order by visit frequency highlights which groups utilize healthcare more intensively. By doing so, we can identify age groups and income ranges with higher healthcare demands, potentially guiding resource allocation and public health policy.</p>

  </div>

  <!-- Section 3: How About You? -->
  <div class="section">
    <div class="section-title">3. How About You?</div>
    <p>Estimate your annual healthcare expenditure by entering some basic information:</p>

    <label>Diabetes Diagnosis:
      <input type="number" bind:value={userInputs.DIABDX_M18} min="0" max="1">
    </label>
    <label>ADHD Diagnosis:
      <input type="number" bind:value={userInputs.ADHDADDX} min="0" max="1">
    </label>
    <label>Asthma Diagnosis:
      <input type="number" bind:value={userInputs.ASTHDX} min="0" max="1">
    </label>
    <label>Family Income:
      <input type="number" bind:value={userInputs.FAMINC22}>
    </label>
    <label>Office-Based Visits:
      <input type="number" bind:value={userInputs.OBTOTV22}>
    </label>
    <label>Age:
      <input type="number" bind:value={userInputs.AGE22X}>
    </label>
    <button on:click={getPrediction}>Get Prediction</button>

    {#if predictedTOTEXP22 !== null}
      <p>Predicted Total Expenditure: ${predictedTOTEXP22.toFixed(2)}</p>
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

  .section p {
    text-align: left;
  }

  .dropdown {
    margin-bottom: 20px;
  }

  .visualization-placeholder {
    font-size: 1em;
    color: var(--text-color);
  }

  .buttons {
    margin-top: 20px;
  }

  button {
    margin: 10px;
    padding: 0.5rem 1rem;
    font-size: 1rem;
    color: white;
    background-color: #333;
    border: none;
    border-radius: 5px;
    cursor: pointer;
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
