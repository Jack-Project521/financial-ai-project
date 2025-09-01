FROM python:3.10

WORKDIR /code/financial-ai-project

# Copy all project contents (current path . , have to run it under the project root directory) to work dir
COPY . /code/financial-ai-project

# Install all package dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the app
CMD ["python", "main.py", "--reload"]