FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE $PORT

CMD streamlit run app.py --server.port $PORT --server.address 0.0.0.0