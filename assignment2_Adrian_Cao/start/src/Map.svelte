<script>
  import * as d3 from 'd3';
  import { legendColor } from 'd3-svg-legend';

  export let data;
  export let fullData;

  let width = 1000;
  let height = 600;

  // Adjust projection for NYC coordinates
  let proj = d3.geoMercator()
    .scale(60000) // Adjusted for NYC scale
    .center([-74.006, 40.7128]) // NYC coordinates
    .translate([width / 2, height / 2]);

  let path = d3.geoPath().projection(proj);

  // Define color scale for population count
  $: scale = d3.scaleQuantile()
  .domain(data.map(d => d.properties.population))
  .range(d3.schemePiYG[9]);

  let legend;
  $: {
    // Configure the legend to match the color scale
    const colorLegend = legendColor()
      .shape('rect')
      .cells(9)
      .scale(scale);

    d3.select(legend).call(colorLegend);
  }
</script>

<main>
  <svg {width} {height}>
    {#each data as d}
      <path style = "fill: {scale(+d.properties.population)};"
        d={path(d)}/>
    {/each}
    {#each fullData as d}
      <path class = "geooverlay"
        d={path(d)}/>
    {/each}

    <!-- Legend for color scale -->
    <g transform="translate({width - 120}, 50)" bind:this={legend} />
  </svg>
</main>

<style>
  .geooverlay {
    stroke: grey;
    stroke-width: 1px;
    fill: none;
  }
</style>
