from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from routes import router

app = FastAPI(title="PawHealth API", version="0.1.0")

@app.middleware("http")
async def normalize_api_prefix(request: Request, call_next):
    if request.scope.get("path", "").startswith("/api/"):
        request.scope["path"] = request.scope["path"][4:] or "/"
    return await call_next(request)

app.include_router(router)


@app.get("/health", summary="Health check")
async def health_check():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root():
    html = """
    <!DOCTYPE html>
    <html lang='en'>
    <head>
        <meta charset='UTF-8'>
        <title>PawHealth API</title>
        <style>
            body {background:#121212;color:#e0e0e0;font-family:Arial,Helvetica,sans-serif;padding:2rem;}
            a {color:#4ab3f4;}
            h1 {color:#fff;}
            .card {background:#1e1e1e;padding:1rem;margin:1rem 0;border-radius:8px;}
            .endpoint {margin-left:1rem;}
        </style>
    </head>
    <body>
        <h1>PawHealth – Track. Analyze. Care.</h1>
        <p>A comprehensive pet health monitoring API.</p>
        <div class='card'>
            <h2>Available Endpoints</h2>
            <ul>
                <li>/health  <span class='endpoint'>GET – health check</span></li>
                <li>/pets/{pet_id}  <span class='endpoint'>GET – pet profile</span></li>
                <li>/ai/analyze  <span class='endpoint'>POST – symptom analysis (AI)</span></li>
                <li>/ai/recommend  <span class='endpoint'>POST – personalized recommendations (AI)</span></li>
            </ul>
        </div>
        <div class='card'>
            <h2>Tech Stack</h2>
            <ul>
                <li>FastAPI 0.115.0</li>
                <li>SQLAlchemy 2.0.35 (PostgreSQL)</li>
                <li>DigitalOcean Serverless Inference (openai-gpt-oss-120b)</li>
                <li>Python 3.12+</li>
            </ul>
        </div>
        <p>Docs: <a href='/docs'>Swagger UI</a> | <a href='/redoc'>ReDoc</a></p>
    </body>
    </html>
    """
    return HTMLResponse(content=html, status_code=200)
