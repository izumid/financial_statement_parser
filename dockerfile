FROM python:3.13.0

# Set the work directory
WORKDIR /

# Copy files to container

COPY requirements.txt .
COPY . /gpt_parser
RUN pip install --no-cache-dir -r requirements.txt

# Expose the listinig port to FastAPI
EXPOSE 5000

# Execute Uvicorn to listinening external requests of container
WORKDIR /gpt_parser
CMD ["uvicorn", "main:app","--port", "5000" , "--host", "0.0.0.0", "--reload"]
