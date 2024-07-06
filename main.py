import pickle
import shutil #保存文檔到本地根目錄上面
import pandas as pd
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse #讓文檔內容能顯示在API上面


app = FastAPI()

model = pickle.load(open('text_classifier.pkl','rb'))
tfidf_vectorizer = pickle.load(open('text_vectorizer.pkl','rb'))
label_encoder = pickle.load(open('text_encoder.pkl','rb'))


@app.post('/upload')
async def uploadFile(file: UploadFile = File(...)):
    with open('test.csv', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {'file_name': file.filename}
    


@app.get('/')
def processor():
    input_df = pd.read_csv('test.csv')
    features = tfidf_vectorizer.transform(input_df['body'])
    preditctions = model.predict(features)
    input_df['category'] = label_encoder.inverse_transform(preditctions) #數字轉變成對應的分類

    output_df = input_df[['id', 'category']]
    output_df.to_csv('result.csv', index=False)


    return FileResponse ('result.csv')




#1 ctrl shift ` => open teminal

#2 cd C:\Users\jade\Udemy\Machine_learning\extract_file_api

#3 python -m venv .venv

## Remove the existing virtual environment
#Remove-Item -Recurse -Force .venv

#4 Activate Virtual Environment 
#.\.venv\Scripts\Activate

#5 If you have a requirements.txt file listing all the dependencies, you can install them with:
#pip install -r requirements.txt
# or pip install scikit-learn==1.2.2

#6 uvicorn main:app --reload


#Note
#1. 不要改變項目的文件夾名稱
#改變後，會無法辨認虛擬環境，無法運行對應的依賴
#建議不要改變名稱

#2. 項目可以運行，但出現黃色波浪紋，指示對應依賴無法被辨認
#解決方法：
#退出VSCode的workspace
#Control + K，然後按 F