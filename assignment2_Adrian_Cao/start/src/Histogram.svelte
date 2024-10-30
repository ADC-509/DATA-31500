<script>
    import * as d3 from 'd3';
  
    export let data;
    export let fullData;
    export let variable; // Snake, Monkey, or Farm Animal
    export let filter;
    export let update;
  
    let margin = {top: 30, right: 30, bottom: 30, left: 40}; // Increase top margin for title
    let width = 360;
    let height = 120; // Adjusted for better scale and multiple histograms
    let chartW = width - margin.left - margin.right;
    let chartH = height - margin.top - margin.bottom;
  
    let brushLayer;
    let xAxis;
    let yAxis;
  
    const brush = d3.brushX()
      .extent([[0, 0], [chartW, chartH]])
      .on("brush", brushed)
      .on("end", brushended);        
  
    function brushed(event) {
      if (event && event.selection) {
        filter = [xScale.invert(event.selection[0]), xScale.invert(event.selection[1])];
        update();
      }
    }
  
    function brushended(event) {
      if (event && !event.selection) {
        filter = [];
        update();
      }
    }
  
    // xScale dynamically adjusted for each animal type's max count
    $: xScale = d3.scaleLinear()
      .range([0, chartW])
      .domain([0, d3.max(fullData, d => d.properties[variable] || 0)]);
  
    $: binData = d3.histogram()
      .value(d => d.properties[variable] || 0)
      .domain(xScale.domain())
      .thresholds(xScale.ticks(10));
  
    $: backgroundBins = binData(fullData);
    $: bins = binData(data);
    
    $: yScale = d3.scaleLinear()
      .range([chartH, 0])
      .domain([0, d3.max(backgroundBins, d => d.length)]);
  
    $: {
      d3.select(brushLayer).call(brush);
      d3.select(xAxis).call(d3.axisBottom(xScale));
      d3.select(yAxis).call(d3.axisLeft(yScale));
    }
  </script>
  
  <main>
    <!-- Add title for the histogram to represent the animal type -->
    <h3 style="text-align: center; color: white;">{variable} Count</h3>
    
    <svg {width} {height}>
      <g transform="translate({margin.left}, {margin.top})">
        <!-- Background bars for full data bins -->
        {#each backgroundBins as d}
          <rect class="backgroundbar"
            x={xScale(d.x0)} 
            y={yScale(d.length)}
            width={xScale(d.x1) - xScale(d.x0)}
            height={chartH - yScale(d.length)}/>
        {/each}
  
        <!-- Foreground bars for filtered data bins -->
        {#each bins as d}
          <rect class="bar"
            x={xScale(d.x0)} 
            y={yScale(d.length)}
            width={xScale(d.x1) - xScale(d.x0)}
            height={chartH - yScale(d.length)}/>
        {/each}
      </g>
  
      <!-- Brush and Axes Layers -->
      <g transform="translate({margin.left}, {margin.top})" bind:this={brushLayer} />
      <g transform="translate({margin.left}, {chartH + margin.top})" bind:this={xAxis} />
      <g transform="translate({margin.left}, {margin.top})" bind:this={yAxis} />
    </svg>
  </main>
  
  <style>
    .bar {
      fill: goldenrod;
      stroke: white;
      stroke-width: 1px;
    }
  
    .backgroundbar {
      fill: grey;
    }
  
    /* Style for the title */
    h3 {
      margin: 0;
      font-size: 14px;
    }
  </style>
  