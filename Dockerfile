FROM python:3.11-slim

# create and activate virtual environment
RUN python3 -m venv /home/code/venv
ENV PATH="/home/code/venv/bin:$PATH"
ENV PYTHONUNBUFFERED 1


# copy requiremets
COPY ./requirements.txt /code/requirements.txt

# install requiremets
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copy app
COPY ./app /code/app

WORKDIR /code/app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
