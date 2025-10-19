# FastAPI Marketplace API

REST API sederhana menggunakan **FastAPI** dengan **JWT Authentication (HS256)**.  
Mendukung login user, akses publik untuk daftar item, dan endpoint terproteksi untuk update profil.

---

##  Setup Environment & Jalankan Server

1. **Install dependencies**
   ```bash
   pip install fastapi uvicorn python-dotenv pyjwt

2. **Membuat .env**
JWT_SECRET=JWT_SECRET=supersecretkey123
port=8000

3. **Menajalankan server**
uvicorn main:app --reload

4. **END POINT API**
| Endpoint      | Method | Proteksi | Deskripsi                           |
| ------------- | ------ | -------- | ----------------------------------- |
| `/auth/login` | POST   | ❌        | Login user dan dapatkan token JWT   |
| `/items`      | GET    | ❌        | Menampilkan daftar item marketplace |
| `/profile`    | PUT    | ✅        | Update profil user (butuh JWT)      |


4. **SCHEMA Request dan Response**
POST /auth/login
Request
{ "email": "demo@example.com", "password": "12345" }
Response (200)
{ "access_token": "<jwt>" }
Response (401)
{ "error": "Invalid credentials" }


PUT /profile
Header
Authorization: Bearer <JWT>
Content-Type: application/json
Request
{ "name": "John Doe" }
Response (200)
{
  "message": "Profile updated",
  "profile": { "name": "John Doe", "email": "demo@example.com" }
}
Response (401)
{ "error": "Token expired" }


5. **Login (dapatkan token)**

curl.exe -X POST "http://127.0.0.1:8000/auth/login" ^
  -H "Content-Type: application/json" ^
  --data-raw "{\"email\":\"demo@example.com\",\"password\":\"12345\"}"


Lihat item

curl.exe -X GET "http://127.0.0.1:8000/items"


Update profil (pakai JWT)

curl.exe -X PUT "http://127.0.0.1:8000/profile" ^
  -H "Authorization: Bearer <ACCESS_TOKEN>" ^
  -H "Content-Type: application/json" ^
  --data-raw "{\"name\":\"John Doe\"}"