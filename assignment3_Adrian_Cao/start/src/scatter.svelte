<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';
  
    export let data = [];
    export let disease;
  
    onMount(() => {
      drawScatterPlot();
    });
  
    $: if (data.length > 0) {
      drawScatterPlot();
    }
  
    function drawScatterPlot() {
      const width = 600;
      const height = 400;
      const margin = { top: 20, right: 30, bottom: 60, left: 80 }; // Increased bottom and left margins for labels
  
      // Clear any existing SVG elements
      d3.select('#scatter').selectAll('*').remove();
  
      // Set color based on disease
      const colorMap = {
        'DIABDX_M18': '#ff7f0e', // Orange for Diabetes
        'ASTHDX': '#1f77b4',     // Blue for Asthma
        'ADHDADDX': '#2ca02c'    // Green for ADHD
      };
      const color = colorMap[disease.code] || '#69b3a2';
  
      // Create scales
      const x = d3.scaleLinear().domain(d3.extent(data, d => d.income)).range([margin.left, width - margin.right]);
      const y = d3.scaleLinear().domain(d3.extent(data, d => d.expenditure)).range([height - margin.bottom, margin.top]);
  
      // Append the SVG element
      const svg = d3
        .select('#scatter')
        .append('svg')
        .attr('width', width)
        .attr('height', height);
  
      // X Axis
      svg.append('g')
        .attr('transform', `translate(0, ${height - margin.bottom})`)
        .call(d3.axisBottom(x).ticks(10))
        .selectAll('text')
        .style('font-size', '12px');
  
      // X Axis Label
      svg.append('text')
        .attr('x', width / 2)
        .attr('y', height - margin.bottom + 40)
        .attr('text-anchor', 'middle')
        .style('font-size', '14px')
        .style('font-weight', 'bold')
        .text('Income Level');
  
      // Y Axis
      svg.append('g')
        .attr('transform', `translate(${margin.left}, 0)`)
        .call(d3.axisLeft(y).ticks(10))
        .selectAll('text')
        .style('font-size', '12px');
  
      // Y Axis Label
      svg.append('text')
        .attr('transform', 'rotate(-90)')
        .attr('x', -height / 2)
        .attr('y', margin.left - 60)
        .attr('text-anchor', 'middle')
        .style('font-size', '14px')
        .style('font-weight', 'bold')
        .text('Total Expenditure');
  
      // Scatter points
      svg.selectAll('circle')
        .data(data)
        .enter()
        .append('circle')
        .attr('cx', d => x(d.income))
        .attr('cy', d => y(d.expenditure))
        .attr('r', 5)
        .attr('fill', color);
    }
  </script>
  
  <div id="scatter"></div>
  
  <style>
    #scatter {
      margin-top: 20px;
    }
  </style>
  