
# Chronic Health Condition Data Story

## Overview

This project is a dynamic, interactive data story exploring healthcare spending and access disparities among individuals with chronic conditions in the U.S. Users can select specific conditions (like diabetes, asthma, or ADHD) and explore how healthcare expenditures and visit frequencies vary by income level and age group.

The web app uses D3.js for data visualization and Svelte for a responsive, interactive interface. This data story is accessible via a public URL on Netlify: [Project URL](https://illustrious-sable-996c54.netlify.app/)

## Key Features

- **Condition-Based Analysis**: Select chronic health conditions to view healthcare expenditure patterns among affected populations.
- **Income-Based Comparison**: Visualize total healthcare expenditures segmented by income, revealing the economic burden distribution.
- **Age Group Filter**: Filter data by age group to observe differences in healthcare utilization across life stages.
- **Interactive Visualization**:
  - Scatter plot and histogram views for healthcare expenditures.
  - A bar chart for medical visit frequencies, with options to sort by income or visit count.
  - Smooth transitions between views to enhance interpretability.
- **Predictive Modeling with Linear Regression**: Initially, we aimed to deploy a Flask API with XGBoost for healthcare expenditure prediction. However, due to technical constraints, this approach proved challenging to integrate. As an alternative, we implemented a simple linear regression model directly within the application, allowing users to estimate their annual healthcare expenditure based on their health data inputs. This linear model offers a straightforward prediction approach and keeps the application self-contained.

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

**Note**: This project is hosted on Netlify at the following URL: [Project URL](https://illustrious-sable-996c54.netlify.app/)

```