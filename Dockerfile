FROM python:3.8

WORKDIR /talkkarivuoro-app

VOLUME /talkkarivuoro-app

# COPY requirements.txt .

RUN python -m venv docker_venv
# RUN source ./docker_venv/bin/activate
# RUN pip install --no-cache-dir -r requirements.txt


# COPY . .

# CMD ["briefcase", "build", "android"]
CMD ["source", "./docker_venv/bin/activate", "&&", "/bin/bash"]
