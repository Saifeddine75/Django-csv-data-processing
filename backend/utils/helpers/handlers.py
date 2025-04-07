import json
import csv
import numpy as np
from datetime import datetime
from io import TextIOWrapper

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from datasets.models import Dataset
from utils.exceptions.HandlerExceptions import (
    # DataValidationError, 
    DataProcessError
)

def compute_stats(values):
    try:
        np_array = np.array(values, dtype=float)
        stats = {
            'min': float(np.min(np_array)),
            'max': float(np.max(np_array)),
            'mean': float(np.mean(np_array)),
            'median': float(np.median(np_array)),
            'std': float(np.std(np_array))
        }
    except DataProcessError:
        raise DataProcessError("Error during compute of: {np_array}\nerr: {exc}")
    
    return stats
    

def parse_csv_to_numpy(file):
    """Parse CSV and return a dictionary with column names as keys and lists as values."""
    file.seek(0)
    csv_file = TextIOWrapper(file, encoding='utf-8')
    reader = csv.DictReader(csv_file)

    columns_data = {key: [] for key in ['timestamp', 'x', 'y', 'z']}
    
    for row in reader:
        try:
            columns_data['timestamp'].append(np.float16(row["timestamp"]))  # Assuming 'ts' column for timestamp
            columns_data['x'].append(np.float16(row["x"]))  # Validate and append x values
            columns_data['y'].append(np.float16(row["y"]))  # Validate and append y values
            columns_data['z'].append(np.float16(row["z"]))  # Validate and append z values
        except KeyError as e:
            print(f"Missing column in row {row}: {e}")

    return {k: np.around(v, decimals=2) for k, v in columns_data.items()}



def mean_aggregation(data: dict[str, np.ndarray], factor=10):
    # Reshape the array into a 2D array where each row contains 'n' elements
    reshaped_arr = data.reshape(-1, factor)

    # Calculate the mean of each row (i.e., mean of each group of 'n' elements)
    reduced_arr = reshaped_arr.mean(axis=1)
    print("new shape", np.shape(reduced_arr))

    return reduced_arr.tolist()


def handle_dataset_file(file):
    """Handle uploaded file and instantiate dataset model with file data."""

    try:
        temp_path = default_storage.save('temp_file.csv', ContentFile(file.read()))
        data_series = parse_csv_to_numpy(file)
        stats = {}

        data_series['norm'] = np.array([np.sqrt(x**2 + y**2 + z**2) for x, y, z in zip(data_series['x'], data_series['y'], data_series['z'])])
        for key in data_series.keys():
            stats[key] = compute_stats(data_series[key])

        aggregate_data = {k: mean_aggregation(v) for k, v in data_series.items()}
        axis_stats = {k: v for k, v in stats.items() if k != 'norm'}

    except DataProcessError as e:
        raise DataProcessError(f"Error processing dataset file: {e}")
    except Exception as e:
        raise DataProcessError(f"Unexpected error: {e}")
    finally:
        default_storage.delete(temp_path)

    Dataset.objects.create(
        title=f"{file.name}-{datetime.now().timestamp()}",
        timestamp=aggregate_data['timestamp'], 
        x=aggregate_data.get('x'), 
        y=aggregate_data.get('y'), 
        z=aggregate_data.get('z'), 
        norm=aggregate_data.get('norm'),
    )
    default_storage.delete(temp_path)
