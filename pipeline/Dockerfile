FROM python
WORKDIR /app
# Create the /logs directory if it doesn't exist
RUN mkdir -p /logs
COPY script.py .
CMD ["python", "script.py"]