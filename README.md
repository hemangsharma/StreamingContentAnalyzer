# StreamingContentAnalyzer
This Streamlit application provides an interactive dashboard for analyzing streaming content data. It allows users to explore movie and TV show ratings, distributions, temporal trends, and genre breakdowns through various visualizations and filters.

## Features

-   **Data Loading:** Reads data from a `data.csv` file.
-   **Sidebar Filters:** <br><br>
    -      Content type (Movie/TV Show) selection.
    -      Genre selection.
    -      Release year range selection.
-   **Key Metrics:** Displays total content count, average rating, and counts for movies and TV shows.
-   **Visualizations:** <br><br>
    -      Rating distribution histogram.
    -      Rating distribution box plot by content type.
    -      Temporal trends of average rating and content count.
    -      Top genres by content count.
    -      Genre distribution treemap.
-   **Data Explorer:** Allows users to view the raw filtered data in a table.
-   **Data Download:** Provides a button to download the filtered data as a CSV file.

## Requirements

-   Python 3.6+
-   Streamlit
-   Pandas
-   Plotly

## Installation

1.  Clone the repository or save the code as a `.py` file.
2.  Ensure you have a `data.csv` file in the same directory as the script.
3.  Install the required Python packages:

    ```bash
    pip install streamlit pandas plotly
    ```

## Usage

1.  Run the Streamlit application:

    ```bash
    streamlit run your_script_name.py
    ```

2.  The application will open in your web browser.
3.  Use the sidebar filters to explore the data.
4.  View the visualizations and key metrics in the main panel.
5.  Use the data explorer to view the raw data.
6.  Download the filtered data as a CSV file using the download button.

## Data Format

The `data.csv` file should contain the following columns:

-   `Type`: Content type (Movie or TV Show).
-   `Genre(s)`: Comma-separated list of genres.
-   `Year`: Release year.
-   `Rating (Out of 5)`: Rating of the content.

## Note

-   Replace `"Your Dataset Name Here"` in the script with the actual name of your dataset.
-   Ensure that the data file is named `data.csv` or modify the script to load the correct file.
-   The application uses custom CSS for styling. You can modify the CSS in the `st.markdown` section to customize the appearance.
