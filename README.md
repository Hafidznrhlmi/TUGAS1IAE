# FastAPI Marketplace API

REST API sederhana menggunakan **FastAPI** dengan **JWT Authentication (HS256)**.  
Mendukung login user, akses publik untuk daftar item, dan endpoint terproteksi untuk update profil.

---

## Setup Environment & Jalankan Server

### 1. Install Dependencies
```bash
pip install fastapi uvicorn python-dotenv pyjwt
```

### 2. Konfigurasi Environment
Buat file `.env` di root project:
```env
JWT_SECRET=supersecretkey123
port=8000
```

### 3. Menjalankan Server
```bash
uvicorn main:app --reload
```

Server akan berjalan di `http://127.0.0.1:8000`

---

## API Endpoints

| Endpoint      | Method | Proteksi | Deskripsi                           |
|---------------|--------|----------|-------------------------------------|
| `/auth/login` | POST   | ❌       | Login user dan dapatkan token JWT   |
| `/items`      | GET    | ❌       | Menampilkan daftar item marketplace |
| `/profile`    | PUT    | ✅       | Update profil user (butuh JWT)      |

---

## Schema Request dan Response

### `POST /auth/login`

**Request Body:**
```json
{
  "email": "demo@example.com",
  "password": "12345"
}
```

**Response (200 OK):**
```json
{
  "access_token": "<jwt_token>"
}
```

**Response (401 Unauthorized):**
```json
{
  "error": "Invalid credentials"
}
```

---

### `GET /items`

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Item 1",
    "price": 10000
  }
]
```

---

### `PUT /profile`

**Headers:**
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "John Doe"
}
```

**Response (200 OK):**
```json
{
  "message": "Profile updated",
  "profile": {
    "name": "John Doe",
    "email": "demo@example.com"
  }
}
```

**Response (401 Unauthorized):**
```json
{
  "error": "Token expired"
}
```

---

## Contoh Penggunaan dengan cURL

### Login (dapatkan token)
```bash
curl.exe -X POST "http://127.0.0.1:8000/auth/login" ^
  -H "Content-Type: application/json" ^
  --data-raw "{\"email\":\"demo@example.com\",\"password\":\"12345\"}"
```

### Lihat Daftar Item
```bash
curl.exe -X GET "http://127.0.0.1:8000/items"
```

### Update Profil (dengan JWT)
```bash
curl.exe -X PUT "http://127.0.0.1:8000/profile" ^
  -H "Authorization: Bearer <ACCESS_TOKEN>" ^
  -H "Content-Type: application/json" ^
  --data-raw "{\"name\":\"John Doe\"}"
```

> **Note:** Ganti `<ACCESS_TOKEN>` dengan token JWT yang didapat dari endpoint login.

---
