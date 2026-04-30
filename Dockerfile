FROM python:3.9

RUN apt-get update && apt-get install -y tcl

WORKDIR /app

COPY . .

RUN pip install streamlit

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
