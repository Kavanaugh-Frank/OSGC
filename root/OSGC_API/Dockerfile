# Use a base image with Miniconda pre-installed from conda-forge
FROM conda/miniconda3

# Set the working directory
WORKDIR /app

# Copy the environment.yml file to the container
COPY environment.yml .

# Create the conda environment specified in environment.yml
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

# Copy the rest of the application code to the container
COPY . .

EXPOSE 8080

# Set the entry point to use the conda environment's Python interpreter
ENTRYPOINT ["conda", "run", "-n", "myenv", "python", "main.py"]
