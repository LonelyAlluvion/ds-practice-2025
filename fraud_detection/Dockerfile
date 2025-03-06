# Use an official Python runtime as the base image
FROM python:3.11

# Set the working directory in the container
# Both the utils and src folders will be mounted as volumes, please see docker-compose.yaml
WORKDIR /app

# Copy the requirements file to the working directory
COPY ./fraud_detection/requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run the application
CMD python utils/other/hotreload.py "fraud_detection/src/app.py"

## 1️⃣ 使用官方 Python 3.11 轻量级版本，减少镜像大小
#FROM python:3.11
#
## 2️⃣ 设置工作目录
#WORKDIR /app
#
## 3️⃣ 复制 requirements.txt 并安装依赖
#COPY ./fraud_detection/requirements.txt .
#
## 4️⃣ 更新 pip 并安装依赖
#RUN pip install --no-cache-dir --upgrade pip \
#    && pip install --no-cache-dir -r requirements.txt
#
## 5️⃣ 复制整个 fraud_detection 目录到容器内
#COPY ./fraud_detection /app/fraud_detection
#
## 6️⃣ 复制 utils 目录到容器内（用于 gRPC 相关）
#COPY ./utils /app/utils
#
## 7️⃣ 暴露端口（gRPC 服务监听的端口）
#EXPOSE 50051
#
## 8️⃣ 运行 gRPC 服务器（去掉热重载，仅用于开发时）
#CMD ["python", "fraud_detection/src/app.py"]
