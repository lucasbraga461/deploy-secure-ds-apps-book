FROM python:3.9.12

WORKDIR /app

COPY . .

# Create a virtual environment, activate and install the requirements
RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout=120", "--workers=3", "wsgi:app"]