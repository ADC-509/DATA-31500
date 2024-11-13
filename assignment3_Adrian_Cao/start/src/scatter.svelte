<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';
  
    export let data = [];
    export let disease;
    export let showScatter = true; // Passed from App.svelte to determine animation
  
    let svgElement;
  
    onMount(() => {
      drawScatterPlot();
    });
  
    $: if (data.length > 0 && showScatter) {
      drawScatterPlot();
    }
  
    function drawScatterPlot() {
      const width = 600;
      const height = 400;
      const margin = { top: 20, right: 30, bottom: 60, left: 80 };
  
      d3.select(svgElement).selectAll('*').remove();
  
      const colorMap = {
        'DIABDX_M18': '#ff7f0e',
        'ASTHDX': '#1f77b4',
        'ADHDADDX': '#2ca02c'
      };
      const color = colorMap[disease.code] || '#69b3a2';
  
      const incomeExtent = d3.extent(data.map(d => d.income));
      const expenditureExtent = d3.extent(data.map(d => d.expenditure));
      const xScale = d3.scaleLinear().domain(incomeExtent).range([margin.left, width - margin.right]);
      const yScale = d3.scaleLinear().domain(expenditureExtent).range([height - margin.bottom, margin.top]);
  
      const svg = d3.select(svgElement)
        .attr('width', width)
        .attr('height', height);
  
      svg.append('g')
        .attr('transform', `translate(0, ${height - margin.bottom})`)
        .call(d3.axisBottom(xScale))
        .append('text')
        .attr('x', width / 2)
        .attr('y', 40)
        .attr('fill', '#000')
        .style('font-size', '14px')
        .style('font-weight', 'bold')
        .text('Income Level');
  
      svg.append('g')
        .attr('transform', `translate(${margin.left}, 0)`)
        .call(d3.axisLeft(yScale))
        .append('text')
        .attr('transform', 'rotate(-90)')
        .attr('x', -height / 2)
        .attr('y', -50)
        .attr('fill', '#000')
        .style('font-size', '14px')
        .style('font-weight', 'bold')
        .text('Total Expenditure');
  
      svg.selectAll('circle')
        .data(data)
        .enter()
        .append('circle')
        .attr('cx', d => xScale(d.income))
        .attr('cy', d => yScale(d.expenditure))
        .attr('r', 5)
        .attr('fill', color)
        .attr("opacity", 1)
        .transition()
        .duration(1000)
        .attr("opacity", showScatter ? 1 : 0); // Fade out dots when transitioning
    }
  </script>
  
  <svg bind:this={svgElement}></svg>
  
  <style>
    svg {
      margin-top: 20px;
    }
  </style>
  