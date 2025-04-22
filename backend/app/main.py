from fastapi import FastAPI 

app = FastAPI()


@app.get("/health")
async def health_check():
    return {"status": "Tudo correto"}



@app.get("/")
async def root():
    return {"messagem": "Bem vindo ao backend do Codesprint"}