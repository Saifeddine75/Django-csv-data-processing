# Project Overview – CSV Data Analysis Web Application

In this project, I developed a full-stack web application designed to analyze and visualize 3D spatial data from CSV files. Each file contains four columns: timestamps, and x, y, z coordinates. The core functionality enables users to upload their CSV file, automatically compute descriptive statistics (min, max, mean, median, standard deviation) for each axis, and calculate the vector norm of the 3D data points.

The application keeps track of previously uploaded files, allowing users to revisit and compare their results easily.

# Key Features

- File upload with automatic parsing and statistical computation
- Persistent results for all past uploads
- Interactive data visualization: plotted x, y, z values and their computed norms on the frontend
- User-friendly interface with a clear and simple design
- Deployed version for easy local access and demonstration

# Tech Stack

Backend: Django REST framework for data processing and API exposure
Containerization: Docker and docker-compose to orchestrate both backend and frontend
Environment Configuration: .env management based on a provided template