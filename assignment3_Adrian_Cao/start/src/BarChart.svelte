<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';
  
    export let visitsData = []; // Data with income and visits properties
    export let condition;
  
    let svgElement;
    let orderByIncome = true; // Default order by income for clear interpretation
    let tooltip; // Tooltip div for hover information
  
    // Watch for changes in visitsData and redraw the chart
    $: if (visitsData.length > 0) {
      drawBarChart();
    }
  
    function drawBarChart() {
      const width = 600;
      const height = 400;
      const margin = { top: 20, right: 30, bottom: 120, left: 80 };
  
      // Define income brackets for color coding
      const colorScale = d3.scaleThreshold()
        .domain([20000, 50000, 100000])
        .range(["#f94144", "#f3722c", "#f9c74f", "#90be6d"]);
  
      // Sort data by income
      const sortedData = orderByIncome
        ? [...visitsData].sort((a, b) => a.income - b.income)
        : [...visitsData].sort((a, b) => a.visits - b.visits);
  
      // Clear previous SVG content
      d3.select(svgElement).selectAll('*').remove();
  
      // Create scales
      const xScale = d3.scaleBand()
        .domain(sortedData.map(d => d.income))
        .range([margin.left, width - margin.right])
        .padding(0.1);
  
      const yScale = d3.scaleLinear()
        .domain([0, d3.max(sortedData, d => d.visits)])
        .nice()
        .range([height - margin.bottom, margin.top]);
  
      const svg = d3.select(svgElement)
        .attr('width', width)
        .attr('height', height);
  
      // X Axis
      svg.append('g')
        .attr('transform', `translate(0, ${height - margin.bottom})`)
        .call(d3.axisBottom(xScale).tickFormat(d3.format(".2s")))
        .selectAll("text")
        .attr("transform", "rotate(-45)")
        .style("text-anchor", "end");
  
      // Y Axis
      svg.append('g')
        .attr('transform', `translate(${margin.left}, 0)`)
        .call(d3.axisLeft(yScale));
  
      // Add bars with color-coding by income bracket and tooltips
      svg.selectAll(".bar")
        .data(sortedData, d => d.income)
        .enter()
        .append("rect")
        .attr("class", "bar")
        .attr("x", d => xScale(d.income))
        .attr("y", height - margin.bottom)
        .attr("width", xScale.bandwidth())
        .attr("height", 0)
        .attr("fill", d => colorScale(d.income)) // Color based on income brackets
        .on("mouseover", (event, d) => showTooltip(event, d))
        .on("mouseout", hideTooltip)
        .transition()
        .duration(800)
        .attr("y", d => yScale(d.visits))
        .attr("height", d => yScale(0) - yScale(d.visits));
    }
  
    // Tooltip setup and helper functions
    onMount(() => {
      tooltip = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);
    });
  
    function showTooltip(event, d) {
      tooltip.transition().duration(200).style("opacity", 1);
      tooltip.html(`Income: ${d3.format("$.2s")(d.income)}<br>Visits: ${d.visits}`)
        .style("left", (event.pageX + 10) + "px")
        .style("top", (event.pageY - 28) + "px");
    }
  
    function hideTooltip() {
      tooltip.transition().duration(500).style("opacity", 0);
    }
  
    // Function to toggle ordering by visits instead of income
    function toggleOrder() {
      orderByIncome = !orderByIncome;
      drawBarChart();
    }
  </script>
  
  <svg bind:this={svgElement}></svg>
  <button on:click={toggleOrder}>
    {orderByIncome ? "Order by Visits" : "Order by Income"}
  </button>
  
  <p class="interpretation">
    {orderByIncome
      ? "This chart is ordered by income levels, helping to illustrate which income groups have more frequent healthcare visits. Higher-income individuals may access healthcare differently than lower-income groups, providing insights into access disparities."
      : "This chart is ordered by the number of visits, showing which groups utilize healthcare more frequently. By observing both income and visit frequency, we can better understand healthcare needs and disparities."
    }
  </p>
  
  <style>
    .bar {
      cursor: pointer;
    }
  
    .tooltip {
      position: absolute;
      text-align: center;
      width: auto;
      padding: 6px;
      background: #333;
      color: #fff;
      border-radius: 4px;
      pointer-events: none;
    }
  
    button {
      margin-top: 10px;
      padding: 5px 10px;
      background-color: #333;
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;
    }
  
    button:hover {
      background-color: #555;
    }
  
    .interpretation {
      margin-top: 20px;
      font-size: 1rem;
      color: #333;
    }
  </style>
  