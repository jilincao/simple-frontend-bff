BFF layer for chatbot service
Library: FastAPI

git clone http://192.168.2.95/jilincao/aift-chatbot-bff-service.git

Production  
`fastapi run` or  
`uvicorn main:app --host 0.0.0.0 --port 9050 --reload`
Dev  
`fastapi dev main.py`

API Docs
http://localhost:9050/docs

Kill a Port
lsof -i:9050
kill -9 2014319

baseUrl="http://192.168.2.97:9050"
API: chat/completions

conda activate /mnt/sgnfsdata/tolo-03-97/jilincao/env/py12