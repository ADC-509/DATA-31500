<script>
  import * as d3 from 'd3';
  import { onMount } from 'svelte';
  import Map from './Map.svelte';
  import Histogram from './Histogram.svelte';

  let data = [];
  let fullData = [];
  let filterSnake = [];
  let filterRooster = [];
  let filterFarmAnimal = [];

  // Focused animal types
  let var1 = 'Snake';
  let var2 = 'Rooster';
  let var3 = 'Farm Animal';

  onMount(async function() {
    // Load data from CSV
    let table = await d3.csv('illegal_animals_kept_as_pets_20241029.csv');

    // Load the GeoJSON file for NYC Zip Code Boundaries
    let geocoord = await d3.json('Modified Zip Code Tabulation Areas (MODZCTA).geojson').then(d => d.features);

    await Promise.all([table, geocoord]).then((values) => {
      let table = values[0];
      let geocoord = values[1];

      // Process each feature in GeoJSON to add counts from CSV
      for (let i = 0; i < geocoord.length; i++) {
        let modzcta = geocoord[i].properties.modzcta;
        let found = false;
        let j = 0;

        // Initialize counts
        let population = 0;
        let snakeCount = 0;
        let RoosterCount = 0;
        let farmanimalCount = 0;

        while (!found && j < table.length) {
          if (table[j]['Incident Zip'] === modzcta) {
            population += 1;

            const descriptor = table[j]['Descriptor'];
            if (descriptor === 'Snake') snakeCount++;
            if (descriptor === 'Rooster') RoosterCount++;
            if (descriptor === 'Farm Animal') farmanimalCount++;
          }
          j++;
        }

        // Attach counts for Snake, Rooster, and Farm Animal to GeoJSON properties
        geocoord[i].properties['population'] = population;
        geocoord[i].properties['Snake'] = snakeCount;
        geocoord[i].properties['Rooster'] = RoosterCount;
        geocoord[i].properties['Farm Animal'] = farmanimalCount;

        data.push(geocoord[i]);
      }

    // console.log(data); 
    // Duplicate the full dataset for filtering purposes
    fullData = [...data];
  });
});

  // Update data based on filters applied
  function updateData() {
  if (filterSnake.length > 0 && filterRooster.length > 0 && filterFarmAnimal.length > 0) {
    data = fullData.filter(d => 
      d.properties['Snake'] >= filterSnake[0] && d.properties['Snake'] < filterSnake[1] &&
      d.properties['Rooster'] >= filterRooster[0] && d.properties['Rooster'] < filterRooster[1] &&
      d.properties['Farm Animal'] >= filterFarmAnimal[0] && d.properties['Farm Animal'] < filterFarmAnimal[1]
    );
  } else if (filterSnake.length > 0 && filterRooster.length > 0) {
    data = fullData.filter(d => 
      d.properties['Snake'] >= filterSnake[0] && d.properties['Snake'] < filterSnake[1] &&
      d.properties['Rooster'] >= filterRooster[0] && d.properties['Rooster'] < filterRooster[1]
    );
  } else if (filterSnake.length > 0 && filterFarmAnimal.length > 0) {
    data = fullData.filter(d => 
      d.properties['Snake'] >= filterSnake[0] && d.properties['Snake'] < filterSnake[1] &&
      d.properties['Farm Animal'] >= filterFarmAnimal[0] && d.properties['Farm Animal'] < filterFarmAnimal[1]
    );
  } else if (filterRooster.length > 0 && filterFarmAnimal.length > 0) {
    data = fullData.filter(d => 
      d.properties['Rooster'] >= filterRooster[0] && d.properties['Rooster'] < filterRooster[1] &&
      d.properties['Farm Animal'] >= filterFarmAnimal[0] && d.properties['Farm Animal'] < filterFarmAnimal[1]
    );
  } else if (filterSnake.length > 0) {
    data = fullData.filter(d => 
      d.properties['Snake'] >= filterSnake[0] && d.properties['Snake'] < filterSnake[1]
    );
  } else if (filterRooster.length > 0) {
    data = fullData.filter(d => 
      d.properties['Rooster'] >= filterRooster[0] && d.properties['Rooster'] < filterRooster[1]
    );
  } else if (filterFarmAnimal.length > 0) {
    data = fullData.filter(d => 
      d.properties['Farm Animal'] >= filterFarmAnimal[0] && d.properties['Farm Animal'] < filterFarmAnimal[1]
    );
  } else {
    data = [...fullData];
  }
}

</script>

<main>
  <h1>NYC Illegal Animals Data</h1>

  <div class="flex-container row">
    <div class="map"><Map data={data} fullData={fullData}></Map></div>
    <div class="flex-container col">
      <div class="hist"><Histogram data={data} fullData={fullData} variable="Rooster" bind:filter={filterRooster} update={updateData}></Histogram></div>
      <div class="hist"><Histogram data={data} fullData={fullData} variable="Farm Animal" bind:filter={filterFarmAnimal} update={updateData}></Histogram></div>
      <div class="hist"><Histogram data={data} fullData={fullData} variable="Snake" bind:filter={filterSnake} update={updateData}></Histogram></div>
    </div>
  </div>
</main>

<style>
  .flex-container {
    display: flex;
    justify-content: center;
    height: 100%;
    padding: 15px;
    gap: 5px;
  }

  .flex-container > div {
    padding: 8px;
  }

  .flex-container .row {
    flex-direction: row;
  }

  .flex-container .col {
    flex-direction: column;
  }

  .map { 
    flex-grow: 1;
  }

  .hist { 
    flex-grow: 0;
  }
</style>
