<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  export let data = [];
  export let disease;
  export let showScatter = true; // Control for animation toggle

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

      const incomeExtent = d3.extent(data, d => d.income);
      const expenditureExtent = d3.extent(data, d => d.expenditure);

      const xScale = d3.scaleLinear().domain(incomeExtent).range([margin.left, width - margin.right]);
      const yScale = d3.scaleLinear().domain(expenditureExtent).range([height - margin.bottom, margin.top]);

      const svg = d3.select(svgElement)
          .attr('width', width)
          .attr('height', height);

      // Define a clipping path
      svg.append("defs")
          .append("clipPath")
          .attr("id", "clip")
          .append("rect")
          .attr("x", margin.left)
          .attr("y", margin.top)
          .attr("width", width - margin.left - margin.right)
          .attr("height", height - margin.top - margin.bottom);

      // Axes
      const xAxisGroup = svg.append('g')
          .attr('transform', `translate(0, ${height - margin.bottom})`)
          .call(d3.axisBottom(xScale));

      xAxisGroup.append('text')
          .attr('x', width / 2)
          .attr('y', 40)
          .attr('fill', '#000')
          .style('font-size', '14px')
          .style('font-weight', 'bold')
          .text('Income Level');

      const yAxisGroup = svg.append('g')
          .attr('transform', `translate(${margin.left}, 0)`)
          .call(d3.axisLeft(yScale));

      yAxisGroup.append('text')
          .attr('transform', 'rotate(-90)')
          .attr('x', -height / 2)
          .attr('y', -50)
          .attr('fill', '#000')
          .style('font-size', '14px')
          .style('font-weight', 'bold')
          .text('Total Expenditure');

      // Group to apply clipping to data points
      const pointsGroup = svg.append('g')
          .attr("clip-path", "url(#clip)");

      const points = pointsGroup.selectAll('circle')
          .data(data)
          .enter()
          .append('circle')
          .attr('cx', d => xScale(d.income))
          .attr('cy', d => yScale(d.expenditure))
          .attr('r', 5)
          .attr('fill', color);

      // Zoom functionality
      const zoom = d3.zoom()
          .scaleExtent([1, 5])
          .on('zoom', (event) => {
              const newXScale = event.transform.rescaleX(xScale);
              const newYScale = event.transform.rescaleY(yScale);
              
              // Update axes
              xAxisGroup.call(d3.axisBottom(newXScale));
              yAxisGroup.call(d3.axisLeft(newYScale));

              // Update positions of points with clipping
              points
                  .attr('cx', d => newXScale(d.income))
                  .attr('cy', d => newYScale(d.expenditure));
          });

      svg.call(zoom);
  }
</script>

<svg bind:this={svgElement}></svg>

<style>
  svg {
    margin-top: 20px;
  }
</style>
