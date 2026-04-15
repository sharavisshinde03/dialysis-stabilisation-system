FROM python:3.10

WORKDIR /app

# Copy only requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Now copy full project
COPY . .

EXPOSE 5000

CMD ["python", "web/app.py"]