# Skipper NDT's software dev test

## Introduction

You will be provided a couple of *.csv files. These files will consist of four columns (timestamps, x, y and z) containing numbers.

The website should allow a user to upload one of the csv files and compute the min, max,
mean, median and standard deviation of each axis as well as the norm.
Those results should be displayed back to the user and the user should be able to go back to the results of previously uploaded files.

Bonus:
- Plot the values of x, y, z and the norm on the frontend
- Deploy the website

## Development

The provided code is a skeleton of the final project you are to deliver. It consists of:

- A Django backend in directory "backend"
- A NextJS frontend in directory "frontend"
- A .env.dist file listing the environment variables you are to provide in a .env file
- A docker-compose.yml file for launching the services

You need to use a Django backend but you can use whatever JS based frontend solution or framework. The one we provide is based on NextJS.


## Evaluation criteria

- Understanding of the assignement
- The solution should be fully functional by following the steps in the README file and ready for deployment (local deployment is sufficient)
- Be prepared to justify your implementation, technological choices and architecture.
- The code should be clear, well structured and easy to read
- The UI should be simple and easy to understand. We value a visually appealing UI design but we understand that this is a time-limited task, so don't spend an excessive amount of time on it.
