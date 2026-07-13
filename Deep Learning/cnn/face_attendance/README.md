# Face Attendance System

This Django project uses OpenCV face detection and recognition to capture user faces, train a face-recognition model, and mark attendance.

## Setup

1. Create and activate the virtual environment:

```bash
cd "/Volumes/E/skill circle/WDNSD23.2/Deep Learning/cnn/face_attendance"
python3 -m venv tf_env
source tf_env/bin/activate
```

2. Install dependencies:

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

3. Run database migrations:

```bash
python manage.py migrate
```

4. Start the development server:

```bash
python manage.py runserver 8000
```

5. Open the app in your browser at `http://127.0.0.1:8000/`.

## Notes

- The project currently defaults to OpenCV LBPH recognition (`USE_TENSORFLOW = False` in `attendance/train_model.py`).
- If you want to enable TensorFlow-based recognition, set `USE_TENSORFLOW = True` in `attendance/train_model.py`.
- Make sure `haarcascade_frontalface_default.xml` is in the project root.
- Face images are saved under `media/faces/<employee_id>/`.

## Workflow

1. Add a user.
2. Capture enough face images.
3. Train the model.
4. Use the attendance page to recognize and mark attendance.
