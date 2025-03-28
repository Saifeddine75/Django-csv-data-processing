from datetime import datetime
import os
import json
import numpy as np

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.views.generic.edit import FormView

from datasets.models import Dataset, DatasetChart
from datasets.utils import compute_chart

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

        timestamps = dataset.timestamp  # Assuming it's a list or queryset of timestamps
        x_values = dataset.x
        y_values = dataset.y
        z_values = dataset.z
        stats = dataset.stats
        norm_values = np.sqrt(np.array(x_values)**2 + np.array(y_values)**2 + np.array(z_values)**2)

        # Prepare data for Highcharts (in JSON format)
        data = {
            'timestamps': timestamps,
            'x_values': x_values,
            'y_values': y_values,
            'z_values': z_values,
            'norm_values': norm_values.tolist(),  # Convert numpy array to list for JSON compatibility
        }

        DatasetChart(
            title=title, 
            data=data,
            created_at=datetime.now()
        )

        return {
            "title": title,
            "timestamps": timestamps,
            "series": [
                {"name": "X", "data": list(zip(timestamps, x_values))},
                {"name": "Y", "data": list(zip(timestamps, y_values))},
                {"name": "Z", "data": list(zip(timestamps, z_values))},
                {"name": "Norm", "data": list(zip(timestamps, norm_values))}
            ],
            'stats': stats
        }

    def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # uploaded_files = os.listdir(settings.MEDIA_ROOT) if os.path.exists(settings.MEDIA_ROOT) else []
        # context["uploaded_files"] = uploaded_files       
        # context["chart_data"] = json.dumps(self.compute_chart())  # Convert chart data to JSON
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

    def view_plots(self, request, file_id):
        # Fetch the CSV file and stats from the database
        chart = self.compute_chart(title=f"dataset-{file_id}", dataset_id=file_id)
        return render(request, 'plot_dataset.html', {'chart': chart})


# class FileFieldFormView(FormView):
#     form_class = FileFieldForm
#     template_name = "pages/upload_file.html"  # Replace with your template.
#     success_url = "."

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # List all uploaded files
#         uploaded_files = os.listdir(settings.MEDIA_ROOT) if os.path.exists(settings.MEDIA_ROOT) else []
#         context["uploaded_files"] = uploaded_files  # Pass files to template
#         return context

#     def post(self, request, *args, **kwargs):
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
        

#     def form_valid(self, form):
#         data = form.cleaned_data
#         try:
#             file = form.cleaned_data["file"]
#             save_path = os.path.join(settings.MEDIA_ROOT, file.name)  # Ensure it saves in MEDIA_ROOT

#             # Save the file properly
#             with open(save_path, "wb+") as destination:
#                 for chunk in file.chunks():
#                     destination.write(chunk)

#         except CustomFileUploadException as e:
#             print(f"File upload failed: {e}")
#             raise 


#         messages.success(self.request, f"File '{file.name}' uploaded successfully!")

#         return super().form_valid(form)

