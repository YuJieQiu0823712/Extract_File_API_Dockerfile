FROM python:3.12
#BaseImage

WORKDIR /app

COPY . /app
#複製所有文件至鏡像裡面
# 需要有對應的python文檔和requiremnets才能製cocker裡面

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD [ "uvicorn", "main:app", "--reload", "--port=8000", "--host=0.0.0.0" ]


