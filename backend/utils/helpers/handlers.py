import csv
from io import TextIOWrapper
import numpy as np

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from datasets.models import Dataset
from utils.exceptions.HandlerExceptions import (
    # DataValidationError, 
    DataProcessError
)


# # TODO: use classes (ask chatgpt)
# def validate(value: float | int):
#     if not value:
#         raise(ValueError(f"Value should not empty: {value}"))
#     try:
#         return float(value)
#     except ValueError as exc:
#         raise DataValidationError(f"Invalid value for conversion: {value}\nerr: {exc}")
    

def compute_stats(values):
    if not values:
        raise ValueError(f"values is empty: {values}")
    try:
        np_array = np.array(values, dtype=np.float64)
        stats = {
            'min': np.min(np_array),
            'max': np.max(np_array),
            'mean': np.mean(np_array),
            'median': np.median(np_array),
            'std': np.std(np_array)
        }
    except DataProcessError:
        raise DataProcessError("Error during compute of: {np_array}\nerr: {exc}")
    
    return stats
    

def parse_csv_to_dict(file):
    """Parse CSV and return a dictionary with column names as keys and lists as values."""
    file.seek(0)
    csv_file = TextIOWrapper(file, encoding='utf-8')
    reader = csv.DictReader(csv_file)
    
    columns_data = {key:[] for key in ['timestamp', 'x', 'y', 'z']}

    for row in reader:
        try:
            columns_data['timestamp'].append(float(row["timestamp"]))  # Assuming 'ts' column for timestamp
            columns_data['x'].append(float(row["x"]))  # Validate and append x values
            columns_data['y'].append(float(row["y"]))  # Validate and append y values
            columns_data['z'].append(float(row["z"]))  # Validate and append z values
        except KeyError as e:
            print(f"Missing column in row {row}: {e}")

    return columns_data

def handle_dataset_file(file):
    """Handle uploaded file and instantiate dataset model with file data."""
    temp_path = default_storage.save('temp_file.csv', ContentFile(file.read()))
    
    # file.seek(0)  # Ensure we start at the beginning of the file
    
    # # Read CSV file
    column_data = parse_csv_to_dict(file)
    # csv_file = TextIOWrapper(file, encoding='utf-8')
    
    # # Process the file from storage
    # reader = csv.DictReader(csv_file)
    # columns = ['timestamp', 'x', 'y', 'z']
    stats = {}

    for column in column_data.keys():
        stats[column] = compute_stats(column_data[column])  # Compute stats for the column
        # Compute norm (Euclidean distance)

    norm = [np.sqrt(x**2 + y**2 + z**2) for x, y, z in zip(column_data['x'], column_data['y'], column_data['z'])]
    norm_stats = compute_stats(norm)
        
    # Create and save the Dataset object
    Dataset.objects.create(
        timestamp=column_data['timestamp'], 
        x=column_data['x'], 
        y=column_data['y'], 
        z=column_data['z'], 
        norm=norm,
        stats={
            'axis':stats, 
            'norm': norm_stats
        }
    )
    default_storage.delete(temp_path)
