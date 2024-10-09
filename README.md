# Currency Rate Fetcher

This Python script fetches daily USD exchange rates from the [Russian Central Bank](https://www.cbr-xml-daily.ru) for a specified number of days (default: 365 days) and saves the data into a CSV file.

## General Information

- **Python Version**: The project is designed for Python 3.9. You can adjust the Python version in Docker settings if necessary.
- **Dependencies**: The project uses the `requests` library for HTTP requests and `pandas` for data handling and CSV export.

## System Requirements

### Without Docker

To run the project locally, ensure the following are installed on your system:

- **Python 3.9** or newer
- **Pip**: Python package installer
- **Required libraries**:
  - `requests`: For handling HTTP requests
  - `pandas`: For data processing and CSV export

You can install the required packages using:

```bash
pip install -r requirements.txt
```

### With Docker

If you prefer to use Docker, ensure the following are installed:

- **Docker**: Installed and properly configured
- **Docker Compose**: For managing multi-container Docker applications

To run the script using Docker Compose:

1. Start the application:

    ```bash
    docker-compose up -d
    ```

2. Access the running container:

    ```bash
    docker-compose exec python-app /bin/bash
    ```

3. Inside the container, run the script:

    ```bash
    python main.py
    ```

The script will fetch USD exchange rates and save the CSV file to the `data` folder, which is mapped to your host system.

## Features

- Fetches daily exchange rates for USD from the Russian Central Bank.
- Saves the data into a CSV file with customizable options.

## Customization

- **CSV Path**: You can customize the path where the CSV is saved by modifying the `CSV_PATH` constant in the script.
- **Date Range**: You can adjust the number of days for which the data is fetched by changing the `DAYS_IN_YEAR` constant.

## Recommended Search Dates

While fetching data, be aware that some dates (such as holidays and weekends) may not have available data. It is recommended to focus on working days (Monday to Friday) to avoid gaps in the dataset. The script will handle missing data gracefully but no entries will be recorded for such days.

## Known Issues

- Data for certain dates (holidays, weekends) may be unavailable. The script will skip missing entries and handle such cases.
- A stable internet connection is required as the script fetches data via external API requests.
