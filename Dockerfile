FROM oraclelinux:10-slim

RUN microdnf install -y python3 python3-pip && \
    microdnf clean all

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY opnsense_config_generator/ ./opnsense_config_generator/
COPY pyproject.toml .
RUN pip3 install --no-cache-dir --no-deps .

WORKDIR /work

ENTRYPOINT ["opnsense-config-generator"]
CMD ["render"]
