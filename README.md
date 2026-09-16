# Relational Traffic Data Analytics Dashboard (Python)

## Project Overview
This project is a menu-driven, query-based Python dashboard engineered to parse, validate, and manipulate public records data from the Stanford Policing Project. The application provides text-based querying and interactive visual assets, operating as a localized database management tool.

## Key Technical Features
* **Automated Data Cleaning & Formatting:** Authored custom functional pipelines to normalize text strings (`.strip().title()`), isolate timestamp details, and cleanly format geographical attributes.
* **Strict Type Validation:** Engineered a relational dictionary mapper (`traffic_stop_record`) that executes rigorous exception handling (`try/except ValueError`) to trap alphanumeric layout anomalies and preserve database consistency.
* **Dynamic Append Operations:** Designed an input architecture that allows user-submitted console inputs to update operational memory arrays dynamically and append records directly to a physical CSV file without corrupting the backend schema.
* **Exploratory Visualizations:** Built automated graphic generation routines using `Plotly.express` to create interactive stacked histograms and geographic plot parameters.

## Core Interface Methods Available
1. **Total Traffic Stops by Gender** (Iterative count query)
2. **Top 5 High-Incident Calendar Days** (Pandas value aggregation)
3. **Top 5 Incident Locations** (Filtered database metrics)
4. **Traffic Outcomes by Gender** (Stacked interactive bar chart)
5. **Top 10 Systemic Violations** (Rotated axis visualization)

## Technologies Used
* **Language:** Python
* **Libraries:** `pandas`, `plotly.express`, `csv`, `os`
