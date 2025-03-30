from datetime import datetime
import json

from django.contrib import messages
from django.views.generic.edit import FormView

from datasets.models import Dataset, DatasetChart

# from .forms import FileFieldForm
from .forms import FileUploadForm
from utils.helpers.handlers import handle_dataset_file

# Create your views here.



class FileUploadView(FormView):
    template_name = "pages/upload_file.html"
    form_class = FileUploadForm
    success_url = "."

    def form_valid(self, form):
        uploaded_file = self.request.FILES["file"]
        # save_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)  # Ensure it saves in MEDIA_ROOT
        # # Save the file properly
        # with open(save_path, "wb+") as destination:
        #     for chunk in uploaded_file.chunks():
        #         destination.write(chunk)
        handle_dataset_file(uploaded_file)
        messages.success(self.request, f"File '{uploaded_file.name}' uploaded successfully!")
        return super().form_valid(form)

    def compute_chart(self, title, dataset_id:str=None):
        """Fetch the latest dataset and compute chart data."""
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_datasets = Dataset.objects.all()

        selected_dataset_id = self.request.GET.get("dataset_id")
        selected_dataset = Dataset.objects.filter(id=selected_dataset_id).first()
        chart_data = self.compute_chart(title="dataset-{selected_dataset_id}", dataset_id=selected_dataset_id) if selected_dataset else None

        context.update({
            "datasets": all_datasets,
            "selected_dataset": selected_dataset,
            "chart_data": json.dumps(chart_data) if chart_data else None,
            "stats": chart_data.get('stats') if chart_data else None
        })
        return context