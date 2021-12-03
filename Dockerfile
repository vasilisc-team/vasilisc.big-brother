FROM python:3.9

ARG GITHUB_SHA

LABEL org.opencontainers.image.source https://github.com/vasilisc-team/vasilisc.big-brother
LABEL com.centurylinklabs.watchtower.lifecycle.post-update="/app/run_report.sh"

# Set language
ENV LANG=en_US.UTF-8
ENV TZ=Europe/Moscow

# Create and activate python venv
ENV VIRTUAL_ENV=/app/env
RUN python3 -m venv ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

# Install dependencies
WORKDIR /app
COPY . .
RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install wheel \
    && python3 -m pip install --no-cache-dir -r requirements/main.txt

# Download models
RUN curl https://github.com/TencentARC/GFPGAN/releases/download/v0.2.0/GFPGANCleanv1-NoCE-C2.pth \
    --output /app/pages/models/data/GFPGANCleanv1-NoCE-C2.pth \
    && curl https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth \
    --output /app/pages/models/data/detection_Resnet50_Final.pth \

# Save git commit hash
RUN echo ${GITHUB_SHA} > .git_commit

EXPOSE 19999
CMD ["python", "./manage.py", "runsslserver", "0.0.0.0:19998", "--static", "--certificate", "/app/certs/certificate.crt", "--key", "/app/certs/certificate.key"]