from datetime import datetime
import numpy as np
from .models import Dataset, DatasetChart


def compute_chart(title:str, dataset: Dataset) -> DatasetChart:
    # Extract data from dataset
    timestamps = dataset.timestamp  # Assuming it's a list or queryset of timestamps
    x_values = dataset.x
    y_values = dataset.y
    z_values = dataset.z
    norm_values = np.sqrt(np.array(x_values)**2 + np.array(y_values)**2 + np.array(z_values)**2)

    # Prepare data for Highcharts (in JSON format)
    data = {
        'timestamps': timestamps,
        'x_values': x_values,
        'y_values': y_values,
        'z_values': z_values,
        'norm_values': norm_values.tolist(),  # Convert numpy array to list for JSON compatibility
    }
    
    chart = DatasetChart(
        title=title, 
        data=data,
        created_at=datetime.now()
    )
    return chart