# NDKTU Student Face Detection API

A production-ready REST API that analyzes video files to detect whether two human faces appear simultaneously in any frame. Built with FastAPI and MediaPipe.

---

## Features

- **`POST /v1/video/analyze`** — Upload a video, receive `{ "has_two_faces": bool }`
- **Efficient frame sampling** — Samples at 2 FPS with early-exit on first match
- **Non-blocking** — OpenCV processing runs off the async event loop
- **Typed error responses** — Every failure maps to a deterministic HTTP status code
- **25 automated tests** — Unit + integration coverage

---

## Requirements

- Python 3.12+
- [`uv`](https://github.com/astral-sh/uv) (recommended) or `pip`

---

## Setup

```bash
# Clone and enter the project
git clone <repo-url>
cd ndktu-student-face-detection

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate
uv sync

# Copy environment config
cp .env.example .env
```

---

## Running

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Interactive API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Usage

```bash
curl -X POST http://localhost:8000/v1/video/analyze \
  -F "file=@your_video.mp4;type=video/mp4"
```

**Response:**

```json
{ "has_two_faces": true }
```

### Supported formats

`mp4`, `avi`, `mov`, `mkv`, `webm` — max **200 MB**

### Error codes

| Code | Reason |
|------|--------|
| `400` | Unsupported format or unreadable/corrupted video |
| `413` | File exceeds 200 MB limit |
| `422` | No file provided |
| `500` | Internal server error |

---

## Project Structure

```
app/
├── main.py              # FastAPI app factory, lifespan, exception handlers
├── core/
│   ├── config.py        # Environment-driven settings (Pydantic)
│   ├── exceptions.py    # Custom exception hierarchy
│   └── logging.py       # Structured logger
├── models/
│   └── schemas.py       # Response schema
├── api/
│   └── v1/
│       └── video.py     # POST /v1/video/analyze
├── services/
│   ├── face_detector.py # MediaPipe Tasks API wrapper
│   └── video_service.py # Analysis pipeline (sampling + detection)
└── utils/
    ├── file_utils.py    # MIME + size validation
    └── video_utils.py   # Frame extraction helpers
tests/
├── unit/                # Mocked logic tests
└── integration/         # HTTP endpoint tests
```

---

## Configuration

All settings are read from `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_PATH` | `blaze_face_short_range.tflite` | Path to MediaPipe model |
| `SAMPLE_FPS` | `2` | Frames per second to sample |
| `MIN_DETECTION_CONFIDENCE` | `0.5` | Minimum face detection confidence |
| `MAX_FILE_SIZE_MB` | `200` | Upload size limit |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

---

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Unit tests only
python -m pytest tests/unit/ -v

# Integration tests only
python -m pytest tests/integration/ -v
```

---

## Detection Logic

1. Video is sampled uniformly at `SAMPLE_FPS` frames per second
2. Each frame is passed through MediaPipe's face detector
3. **Returns `true`** on the first frame where exactly **2 faces** are detected simultaneously
4. **Returns `false`** if no such frame exists (0, 1, or 3+ faces in all frames)

Corrupted frames are skipped silently; the analysis continues on remaining frames.
