# NYC Illegal Animals as Pets Data Visualization

This project visualizes data on illegal animals kept as pets across New York City, organized by census regions. Using **D3.js** and **Svelte**, the app presents an interactive map and histograms, allowing users to explore data on specific animal types, including **Snake**, **Rooster**, and **Farm Animal**.

## Features

- **Interactive Choropleth Map**: A map of NYC displays population densities of illegal animals kept as pets, color-coded by density.
- **Filterable Histograms**: Three histograms show the count of incidents for Snakes, Roosters, and Farm Animals by region, with adjustable filters for detailed exploration.
- **Dynamic Legend**: The map legend automatically adjusts based on data distribution, showing minimum and maximum values in each color range.

## Live Demo

Explore the live app here: [NYC Illegal Animals Data Visualization on Netlify](https://ubiquitous-bienenstitch-0e8bac.netlify.app/)

## Data

The dataset includes information on illegal pets categorized by type and census region. Data includes:
- **Animal Types**: Specific categories such as Snake, Rooster, and Farm Animal.
- **Incident Counts**: Aggregated counts for each census region, representing the density of illegal animals.

## Technologies Used

- **Svelte**: For a reactive UI framework.
- **D3.js**: For scales, color schemes, and data-driven document manipulation.
- **GeoJSON**: For NYC census region boundaries used in the map.

## Project Setup

1. **Install Dependencies**:
   ```bash
   npm install
   ```
2. **Run Development Server**:
   ```bash
   npm run dev
   ```
3. **Build for Production**:
   ```bash
   npm run build
   ```

## Deployment on Netlify

To deploy the application, we used [Netlify](https://www.netlify.com/) for hosting the static site, generated through Vite. The current live site URL is [here](https://ubiquitous-bienenstitch-0e8bac.netlify.app/).

## License

This project is licensed under the MIT License.
```

---

### Creating the Zip File

1. **Prepare Files**: Ensure your project folder includes all code, data files, and the `README.md`.
2. **Compress the Folder**: Select the project folder, right-click, and choose “Send to > Compressed (zipped) folder” on Windows or “Compress” on macOS.
3. **Upload to Gradescope**: Log in to Gradescope, navigate to the assignment, and upload the zip file.

This setup should meet the requirements for your submission. Let me know if you need further assistance!
