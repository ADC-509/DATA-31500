<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  export let data = [];
  export let disease;
  export let showScatter = false; // Passed from App.svelte to control animation

  let svgElement;

  onMount(() => {
      drawHistogram();
  });

  $: if (data.length > 0 && !showScatter) {
      drawHistogram();
  }

  function drawHistogram() {
      const width = 600;
      const height = 400;
      const margin = { top: 20, right: 30, bottom: 60, left: 80 };

      // Clear previous SVG content
      d3.select(svgElement).selectAll('*').remove();

      // Color based on disease
      const colorMap = {
          'DIABDX_M18': '#ff7f0e',
          'ASTHDX': '#1f77b4',
          'ADHDADDX': '#2ca02c'
      };
      const color = colorMap[disease.code] || '#69b3a2';

      const expenditureExtent = d3.extent(data.map(d => d.expenditure));
      const xScale = d3.scaleLinear().domain(expenditureExtent).range([margin.left, width - margin.right]).nice();
      const bins = d3.histogram().value(d => d.expenditure).domain(xScale.domain()).thresholds(xScale.ticks(12))(data);
      const yScale = d3.scaleLinear().domain([0, d3.max(bins, d => d.length)]).range([height - margin.bottom, margin.top]);

      const svg = d3.select(svgElement)
          .attr('width', width)
          .attr('height', height);

      // X Axis
      svg.append('g')
          .attr('transform', `translate(0, ${height - margin.bottom})`)
          .call(d3.axisBottom(xScale))
          .append('text')
          .attr('x', width / 2)
          .attr('y', 40)
          .attr('fill', '#000')
          .style('font-size', '14px')
          .style('font-weight', 'bold')
          .text('Expenditure (Binned)');

      // Y Axis
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
          .text('Count');

      // Transition circles from scatter to histogram
      const circles = svg.selectAll('circle')
          .data(data)
          .join('circle')
          .attr('cx', d => xScale(d.expenditure)) // Start with scatter's x position
          .attr('cy', d => yScale(0)) // Start at baseline of y axis
          .attr('r', 5)
          .attr('fill', color)
          .attr('opacity', 1)
          .transition()
          .duration(1000)
          .attr('cy', d => {
              const bin = bins.find(bin => bin.x0 <= d.expenditure && bin.x1 > d.expenditure);
              return bin ? yScale(bin.length) : height - margin.bottom;
          })
          .attr('opacity', 0); // Fade out circles

      // Draw bars for the histogram with an animation
      svg.selectAll('rect')
          .data(bins)
          .enter()
          .append('rect')
          .attr('x', d => xScale(d.x0) + 1)
          .attr('width', d => xScale(d.x1) - xScale(d.x0) - 1)
          .attr('y', height - margin.bottom)
          .attr('height', 0)
          .attr('fill', color)
          .transition()
          .delay(500)
          .duration(1000)
          .attr('y', d => yScale(d.length))
          .attr('height', d => yScale(0) - yScale(d.length));
  }
</script>

<svg bind:this={svgElement}></svg>

<style>
  svg {
      margin-top: 20px;
  }
</style>
