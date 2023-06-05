FROM python:3.9

COPY . .

# minizinc 2.5.3 -> requires python library minizinc in version 0.8.0 (not 0.9.0)
# https://github.com/MiniZinc/minizinc-python/releases
RUN apt-get update && apt-get install -y --no-install-recommends minizinc

WORKDIR /python

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["python", "-u", "Server.py"]