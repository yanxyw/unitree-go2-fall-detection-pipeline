## Running the Mobile App

### 1. Ensure Flutter SDK is Installed

```bash
flutter --version
```

### 2. Install Flutter Dependencies

```bash
flutter pub get
```

### 3. Configure Firebase

Download the google-services.json file from your Firebase Console and place it in:

```bash
mobile/android/app/google-services.json
```
⚠️ This file is required for Firebase features like push notifications to work.

### 4. Run the App
To run on an Android emulator or connected device:

```bash
flutter run
```
