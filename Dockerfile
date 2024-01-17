# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# 安装 Jupyter Notebook
RUN pip install jupyterlab

# 下载chorme 和chormedriver
RUN wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/linux64/chrome-linux64.zip
RUN unzip chrome-linux64.zip
RUN mv chrome-linux64/chrome /usr/bin/chrome
RUN chown root:root /usr/bin/chrome
RUN chmod +x /usr/bin/chrome

RUN wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/linux64/chromedriver-linux64.zip
RUN unzip chromedriver-linux64.zip
RUN mv chromedriver-linux64 /usr/bin/chromedriver
RUN chown root:root /usr/bin/chromedriver
RUN chmod +x /usr/bin/chromedriver


WORKDIR /ai_news
COPY . /ai_news

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /ai_news
USER appuser

# 暴露端口
EXPOSE 8888

# 运行 Jupyter Notebook
CMD ["jupyter", "lab", "--ip", "0.0.0.0", "--port", "8888", "--allow-root","--NotebookApp.token=password"]
