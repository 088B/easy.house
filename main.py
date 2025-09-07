import os
import base64
import uuid
import json
import io
import logging
from typing import Optional
from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image
from dotenv import load_dotenv
from openai import OpenAI
from .utils import points_to_mask

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
<<<<<<< HEAD

# Load .env
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY not set in environment (.env).")
    raise RuntimeError('OPENAI_API_KEY is missing. Create .env and set your key.')

# Initialize OpenAI client (1.x style)
client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI(title='Virtual House Inserter')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
GENERATED_DIR = os.path.join(PROJECT_ROOT, 'generated')
os.makedirs(GENERATED_DIR, exist_ok=True)

app.mount('/static', StaticFiles(directory=os.path.join(BASE_DIR, 'static')), name='static')
app.mount('/generated', StaticFiles(directory=GENERATED_DIR), name='generated')
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, 'templates'))

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.post('/api/edit')
async def edit_image(
    request: Request,
    prompt: str = Form(...),
    points: str = Form(...),
    image: UploadFile = File(...),
    size: Optional[str] = Form(None),
    output_format: Optional[str] = Form('png'),
    quality: Optional[str] = Form(None),
):
    try:
        raw = await image.read()
        with Image.open(io.BytesIO(raw)) as im:
            im = im.convert('RGBA')
            try:
                pts = json.loads(points)
                polygon = [(float(p['x']), float(p['y'])) for p in pts]
            except Exception as e:
                raise HTTPException(status_code=400, detail=f'Invalid points format: {e}')
            if len(polygon) < 3:
                raise HTTPException(status_code=400, detail='Please select at least 3 points.')
            mask_img = points_to_mask(im, polygon)

            tmp_id = str(uuid.uuid4())
            input_path = os.path.join(GENERATED_DIR, f'{tmp_id}_input.png')
            mask_path = os.path.join(GENERATED_DIR, f'{tmp_id}_mask.png')
            output_ext = 'png' if (output_format or 'png').lower() == 'png' else 'jpg'
            output_path = os.path.join(GENERATED_DIR, f'{tmp_id}_output.{output_ext}')

            im.save(input_path, format='PNG')
            mask_img.save(mask_path, format='PNG')

        final_prompt = prompt.strip() + '\n\n' + (
            'Insert a realistic, properly scaled house inside ONLY the transparent masked region. '
            'Preserve the rest of the photo exactly. Match perspective, lighting, and shadows.'
        )

        # Call OpenAI (1.x client pattern)
        with open(input_path, 'rb') as input_img, open(mask_path, 'rb') as mask_file:
            logger.info("Calling OpenAI images.edit...")
            resp = client.images.edit(
                model="gpt-image-1",
                image=input_img,
                mask=mask_file,
                prompt=final_prompt,
                size=size if size and size.lower() != 'auto' else None,
                quality=quality
            )

        logger.debug("OpenAI response: %s", getattr(resp, "__dict__", str(resp)))

        # response may contain base64
        b64 = None
        try:
            b64 = resp.data[0].b64_json
        except Exception:
            # Some endpoints/versions return url instead
            try:
                b64 = resp.data[0].url  # fallback
            except Exception:
                b64 = None

        if not b64:
            raise HTTPException(status_code=500, detail='OpenAI did not return an image (empty response).')

        # if b64 looks like base64 (contains only base64 chars), decode; if it's a url, fetch it
        if b64.startswith("http://") or b64.startswith("https://"):
            # fetch it (use requests)
            import requests
            r = requests.get(b64)
            if r.status_code != 200:
                raise HTTPException(status_code=500, detail=f'Failed to download image from OpenAI url: {r.status_code}')
            with open(output_path, 'wb') as f:
                f.write(r.content)
        else:
            img_bytes = base64.b64decode(b64)
            with open(output_path, 'wb') as f:
                f.write(img_bytes)

        rel_url = f"/generated/{os.path.basename(output_path)}"
        return JSONResponse({'ok': True, 'url': rel_url})
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error in /api/edit")
        raise HTTPException(status_code=500, detail=str(e))

=======

# Load .env
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY not set in environment (.env).")
    raise RuntimeError('OPENAI_API_KEY is missing. Create .env and set your key.')
    

# Initialize OpenAI client (1.x style)
client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI(title='Virtual House Inserter')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
GENERATED_DIR = os.path.join(PROJECT_ROOT, 'generated')
os.makedirs(GENERATED_DIR, exist_ok=True)

app.mount('/static', StaticFiles(directory=os.path.join(BASE_DIR, 'static')), name='static')
app.mount('/generated', StaticFiles(directory=GENERATED_DIR), name='generated')
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, 'templates'))

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.post('/api/edit')
async def edit_image(
    request: Request,
    prompt: str = Form(...),
    points: str = Form(...),
    image: UploadFile = File(...),
    size: Optional[str] = Form(None),
    output_format: Optional[str] = Form('png'),
    quality: Optional[str] = Form(None),
):
    try:
        raw = await image.read()
        with Image.open(io.BytesIO(raw)) as im:
            im = im.convert('RGBA')
            try:
                pts = json.loads(points)
                polygon = [(float(p['x']), float(p['y'])) for p in pts]
            except Exception as e:
                raise HTTPException(status_code=400, detail=f'Invalid points format: {e}')
            if len(polygon) < 3:
                raise HTTPException(status_code=400, detail='Please select at least 3 points.')
            mask_img = points_to_mask(im, polygon)

            tmp_id = str(uuid.uuid4())
            input_path = os.path.join(GENERATED_DIR, f'{tmp_id}_input.png')
            mask_path = os.path.join(GENERATED_DIR, f'{tmp_id}_mask.png')
            output_ext = 'png' if (output_format or 'png').lower() == 'png' else 'jpg'
            output_path = os.path.join(GENERATED_DIR, f'{tmp_id}_output.{output_ext}')

            im.save(input_path, format='PNG')
            mask_img.save(mask_path, format='PNG')

        final_prompt = prompt.strip() + '\n\n' + (
            'Insert a realistic, properly scaled house inside ONLY the transparent masked region. '
            'Preserve the rest of the photo exactly. Match perspective, lighting, and shadows.'
        )

        # Call OpenAI (1.x client pattern)
        with open(input_path, 'rb') as input_img, open(mask_path, 'rb') as mask_file:
            logger.info("Calling OpenAI images.edit...")
            resp = client.images.edit(
                model="gpt-image-1",
                image=input_img,
                mask=mask_file,
                prompt=final_prompt,
                size=size if size and size.lower() != 'auto' else None,
                quality=quality
            )

        logger.debug("OpenAI response: %s", getattr(resp, "__dict__", str(resp)))

        # response may contain base64
        b64 = None
        try:
            b64 = resp.data[0].b64_json
        except Exception:
            # Some endpoints/versions return url instead
            try:
                b64 = resp.data[0].url  # fallback
            except Exception:
                b64 = None

        if not b64:
            raise HTTPException(status_code=500, detail='OpenAI did not return an image (empty response).')

        # if b64 looks like base64 (contains only base64 chars), decode; if it's a url, fetch it
        if b64.startswith("http://") or b64.startswith("https://"):
            # fetch it (use requests)
            import requests
            r = requests.get(b64)
            if r.status_code != 200:
                raise HTTPException(status_code=500, detail=f'Failed to download image from OpenAI url: {r.status_code}')
            with open(output_path, 'wb') as f:
                f.write(r.content)
        else:
            img_bytes = base64.b64decode(b64)
            with open(output_path, 'wb') as f:
                f.write(img_bytes)

        rel_url = f"/generated/{os.path.basename(output_path)}"
        return JSONResponse({'ok': True, 'url': rel_url})
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error in /api/edit")
        raise HTTPException(status_code=500, detail=str(e))
