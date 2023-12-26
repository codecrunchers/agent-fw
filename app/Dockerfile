FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
ENV VIRTUAL_ENV=/opt/venv
RUN python3  -m venv --system-site-packages $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY ./requirements.txt /app/requirements.txt
RUN python3 -m pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./app /app

