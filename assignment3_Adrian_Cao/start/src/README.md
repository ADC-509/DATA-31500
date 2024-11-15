
# Chronic Health Condition Data Story

## Overview

This project is a dynamic, interactive data story exploring healthcare spending and access disparities among individuals with chronic conditions in the U.S. Users can select specific conditions (like diabetes, asthma, or ADHD) and explore how healthcare expenditures and visit frequencies vary by income level and age group.

The web app uses D3.js for data visualization and Svelte for a responsive, interactive interface. This data story is accessible via a public URL on Netlify: [Project URL](https://clever-peony-4110fe.netlify.app/)

## Key Features

- **Condition-Based Analysis**: Choose specific chronic health conditions to explore patterns in healthcare expenditures among different populations.
- **Income-Based Comparison**: Visualize healthcare expenditures segmented by income levels to uncover the economic burdens faced by various groups.
- **Age Group Filter**: Filter data by age group to examine variations in healthcare utilization across life stages.
- **Interactive Visualization**:
  - Toggle between scatter plot and histogram views for healthcare expenditures.
  - Use a bar chart to compare medical visit frequencies, with options to sort by income level or visit count.
  - Smooth transitions between visualization views enhance interpretability.
  - **Zoom Functionality**: On the scatter plot, zoom in to focus on specific income and expenditure clusters for detailed analysis.
- **In-Text Statistics**: Hover over condition names in the narrative to see live statistics—such as total cases and average income or expenditure—based on the selected chronic condition, helping users gain insights directly within the context of the discussion.
- **Predictive Modeling with Linear Regression**: Initially, an XGBoost model deployed via Flask API was considered for healthcare expenditure prediction. However, due to integration challenges, a simpler linear regression model was implemented directly in the application. This model provides users with expenditure estimates based on their input data, offering a self-contained prediction tool for personalized insights.

## Data Source

The data is derived from the `MEPS HC-243: 2022 Full Year Consolidated Data File`, which contains information on medical expenditures and utilization for individuals with chronic conditions in the U.S. This dataset is enriched with demographic information (income, age) and health-related variables, providing a comprehensive view of healthcare disparities.

## Future Enhancements

- **Predictive Modeling with Machine Learning**: An exciting future direction is to implement machine learning to estimate annual healthcare expenditure based on user-provided health data. This could involve feature engineering, weight adjustments, and potentially a deep learning model to handle the complexities of the survey data. Due to time constraints and the model training complexity, this feature was deferred.
  
  **Possible Challenges**:
  - The dataset has many features, requiring significant preprocessing.
  - Applying deep learning to weighted survey data is complex due to potential overfitting risks and data imbalances.
  
- **User-Input Customization**: Allow users to input their own demographic and health information to receive personalized healthcare expenditure estimates, based on the predictive model mentioned above.
  
- **Expanded Condition List**: Add more chronic conditions or customize condition combinations to broaden the analysis and offer insights into co-morbidities.

- **Enhanced Data Insights**: Add statistical summaries, trends, or comparisons to highlight disparities in healthcare spending and access more explicitly.

## License

This project is licensed under the MIT License.

---

**Note**: This project is hosted on Netlify at the following URL: [Project URL](https://clever-peony-4110fe.netlify.app/)

```