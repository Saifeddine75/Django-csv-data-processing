from datetime import datetime
import json

from django.contrib import messages
from django.views.generic.edit import FormView
from django.core.serializers import serialize

from datasets.models import Dataset, DatasetChart

from .forms import FileUploadForm
from utils.helpers.handlers import handle_dataset_file

from django.shortcuts import redirect
from .models import Dataset  # Ensure you import your Dataset model
# Create your views here.



class DatasetUploadView(FormView):
    template_name = "pages/dataset_plot.html"
    form_class = FileUploadForm
    success_url = "."

    def form_valid(self, form):
        uploaded_file = self.request.FILES["file"]
        handle_dataset_file(uploaded_file)
        messages.success(self.request, f"File '{uploaded_file.name}' uploaded successfully!")
        return super().form_valid(form)

    def compute_dataset_chart(self, title:str, dataset_id:str=None):
        """Compute chart for the given dataset_id or the latest dataset."""
        if not dataset_id:
            dataset = Dataset.objects.last()
        else:
            dataset = Dataset.objects.filter(id=dataset_id).first()

        stats = dataset.stats
        plot_data = {
            "title": title,
            "timestamps": dataset.timestamp,
            "series": [
                {"name": "X", "data": list(zip(dataset.timestamp, dataset.x))},
                {"name": "Y", "data": list(zip(dataset.timestamp, dataset.y))},
                {"name": "Z", "data": list(zip(dataset.timestamp, dataset.z))},
                {"name": "Norm", "data": list(zip(dataset.timestamp, dataset.norm))}
            ],
            'stats': stats
        }
        DatasetChart(
            title=title,
            plot_data=plot_data,
            stats=stats,
            created_at=datetime.now()
        )
        return plot_data

    def delete_dataset(self, dataset_id:int=None):
        if dataset_id:
            dataset = Dataset.objects.filter(id=dataset_id).first()
            dataset.delete()
            messages.success(self.request, f"Dataset {dataset_id} deleted successfully!")
        return redirect("upload_dataset")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_datasets = Dataset.objects.all()
        selected_dataset = []

        selected_dataset_id = self.request.GET.get("dataset_id")
        if selected_dataset_id:
            selected_dataset = Dataset.objects.get(id=selected_dataset_id)

        chart_data = self.compute_dataset_chart(title="dataset-{selected_dataset_id}", dataset_id=selected_dataset_id) if selected_dataset else None

        context.update({
            "datasets": serialize("json", all_datasets),
            "selected_dataset": serialize("json", selected_dataset),
            "chart_data": json.dumps(chart_data) if chart_data else None,
            "stats": chart_data.get('stats') if chart_data else None
        })
        return context
    
