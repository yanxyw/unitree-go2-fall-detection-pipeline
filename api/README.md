## Running the FastAPI Notification Server

### 1. Create and activate a Conda environment

```bash
conda create -n fall-api python=3.11
conda activate fall-api
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up Firebase Admin SDK

- Go to the [Firebase Console](https://console.firebase.google.com/) and open your project.
- Navigate to **Project Settings** → **Service accounts**.
- Click **“Generate new private key”** under the **Firebase Admin SDK** section.
- Download the JSON file, rename it to:

  ```text
  unitree-go2-fcm.json
  ```

- Place the file in the **root directory** of this project.

### 4. Run the app

```bash
uvicorn main:app --reload
```

### 5. Access the API

- Main endpoint: [http://localhost:8000](http://localhost:8000)  
- Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)
