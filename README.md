# Streamlit CI App

This is a Streamlit app for gathering and presenting results in charts of performance data from the Google Search Console API for control and experimental groups.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/streamlit-ci-app.git
   ```

2. Install the required packages:

   ```bash 
   pip install -r requirements.txt
   ```

3. Set up the Google Search Console API credentials:

   - Follow the instructions in the Google Search Console API documentation to create a new project and enable the Search Console API.
   - Download the client_secret.json file and save it in the root directory of the project.

## Usage

1. Run the app:

   ```bash
   streamlit run app.py
   ```

2. Enter the required information:

   - Enter the set of website URLs for the control and experimental groups.
   - Enter the date range for the performance data.
   - Click the "Get Data" button to retrieve the data from the Google Search Console API.

3. View the results:

   - The app will display charts of the performance data for the control and experimental groups.

## Contributing

Contributions are welcome! Please see the contributing guidelines for more information.

## License
This project is licensed under the MIT License.
