# 🔗 URL Shortener

A simple, fast, and reliable **URL Shortener API** built with **Python and FastAPI**.

This project converts long URLs into short, easy-to-share links. It also provides an API to create short URLs, redirect users to the original URLs, and retrieve URL information.

---

## 🚀 Features

* 🔗 Convert long URLs into short URLs
* ⚡ Fast API powered by FastAPI
* 🔄 Automatic redirection from short URL to original URL
* 🆔 Unique short-code generation
* 📊 Track basic URL information
* 🗄️ Persistent database storage
* ✅ URL validation
* 📖 Interactive API documentation with Swagger UI
* 🧩 Clean and modular project structure

---

## 🛠️ Tech Stack

| Technology     | Purpose                       |
| -------------- | ----------------------------- |
| **Python**     | Core programming language     |
| **FastAPI**    | Backend REST API framework    |
| **Pydantic**   | Data validation               |
| **SQLAlchemy** | Database ORM                  |
| **SQLite**     | Database                      |
| **Uvicorn**    | ASGI server                   |
| **Swagger UI** | Interactive API documentation |

---


## ⚙️ How It Works

The URL shortening process is straightforward:

```text
Original URL
     │
     ▼
POST /shorten
     │
     ▼
Validate URL
     │
     ▼
Generate Unique Short Code
     │
     ▼
Store URL in Database
     │
     ▼
Return Short URL
```

When a user opens the generated short URL:

```text
Short URL
    │
    ▼
GET /{short_code}
    │
    ▼
Find Original URL
    │
    ▼
Redirect User
    │
    ▼
Original Website
```

---

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/hiteshjha24/url-shortener.git
```

Navigate into the project:

```bash
cd url-shortener
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Start the FastAPI server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

## 📚 API Documentation

Once the server is running, FastAPI automatically provides interactive documentation.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

You can use Swagger UI to test the API endpoints directly from your browser.

---

# 📡 API Endpoints

## 1. Create a Short URL

### `POST /shorten`

Creates a new shortened URL.

### Request

```json
{
    "url": "https://www.example.com/very/long/url"
}
```

### Response

```json
{
    "short_code": "aB72xK",
    "short_url": "http://127.0.0.1:8000/aB72xK",
    "original_url": "https://www.example.com/very/long/url"
}
```

---

## 2. Redirect to Original URL

### `GET /{short_code}`

Redirects the user to the original URL associated with the short code.

### Example

```text
http://127.0.0.1:8000/aB72xK
```

The server looks up `aB72xK` in the database and redirects the user to the stored original URL.

---

## 3. Get URL Information

### `GET /info/{short_code}`

Returns information about a shortened URL.

### Example Response

```json
{
    "short_code": "aB72xK",
    "original_url": "https://www.example.com/very/long/url",
    "created_at": "2026-08-11T12:30:00",
    "clicks": 15
}
```

---

# 🗄️ Database

The application stores shortened URLs in a database.

A typical URL record contains:

| Field          | Description                                |
| -------------- | ------------------------------------------ |
| `id`           | Unique database ID                         |
| `original_url` | Original long URL                          |
| `short_code`   | Generated short identifier                 |
| `created_at`   | URL creation timestamp                     |
| `clicks`       | Number of times the short URL was accessed |

Example:

```text
┌────┬──────────────────────────┬────────────┬────────┐
│ ID │ Original URL             │ Short Code │ Clicks │
├────┼──────────────────────────┼────────────┼────────┤
│ 1  │ https://example.com/...  │ aB72xK     │ 15     │
│ 2  │ https://github.com/...   │ X9kLm2     │ 8      │
└────┴──────────────────────────┴────────────┴────────┘
```

---

# 🔐 Short Code Generation

Each URL receives a unique short code.

For example:

```text
https://www.example.com/some/very/long/url
                    ↓
                 aB72xK
                    ↓
http://localhost:8000/aB72xK
```

The short code is designed to be:

* Short
* Unique
* URL-safe
* Easy to store
* Fast to look up

---

# 🧪 Testing

Run the test suite using:

```bash
pytest
```

For more detailed output:

```bash
pytest -v

---

# ☁️ Deploying with Vercel

The repository is configured as two Vercel projects: one for the FastAPI backend and one for the Vite frontend. Use a hosted Postgres database because Vercel's filesystem is ephemeral and SQLite data will not persist between deployments.

## 1. Create the database

Neon, Supabase, or another managed PostgreSQL provider works. Neon is a simple option:

1. Create an account at [neon.tech](https://neon.tech) and create a project.
2. Copy the pooled or direct connection string. It should look like `postgresql://user:password@host/database?sslmode=require`.
3. Keep this value private. It will be added to Vercel as `DATABASE_URL`.

Redis is optional. The app treats Redis connection failures as cache misses. Add an Upstash Redis database later if you want caching and set `REDIS_HOST` and `REDIS_PORT` accordingly.

## 2. Deploy the backend

1. In Vercel, select **Add New Project**, import this Git repository, and name the project (for example, `url-shortener-api`).
2. Leave the project root at the repository root. The included `vercel.json` and `api/index.py` configure the FastAPI function.
3. Add these Production environment variables:

    ```text
    DATABASE_URL=postgresql://user:password@host/database?sslmode=require
    SECRET_KEY=<long-random-secret>
    CORS_ORIGINS=https://<your-frontend-project>.vercel.app
    ```

4. Deploy and copy the backend URL, for example `https://url-shortener-api.vercel.app`.

## 3. Run the database migrations

Run this from the repository root on your machine with the same database URL:

```powershell
$env:DATABASE_URL = "postgresql://user:password@host/database?sslmode=require"
python -m pip install -r requirements.txt
alembic upgrade head
```

The command creates the `urls`, `users`, and Alembic version tables. Run it once before using the deployed API, and run it again after adding future migrations.

## 4. Deploy the frontend

1. Create a second Vercel project from the same repository.
2. Set **Root Directory** to `frontend`.
3. Vercel should detect Vite. Use `npm run build` as the build command and `dist` as the output directory.
4. Add this Production environment variable:

    ```text
    VITE_API_BASE_URL=https://<your-backend-project>.vercel.app/api/v1
    ```

5. Deploy. The included `frontend/vercel.json` keeps React Router routes working on direct page refreshes.

## 5. Finish CORS setup

Copy the final frontend Vercel URL into the backend project's `CORS_ORIGINS` variable. Redeploy the backend after changing it. For a custom frontend domain, use that domain instead of the temporary `vercel.app` URL.

## Local environment files

Copy `.env.example` to `.env` for the backend and `frontend/.env.example` to `frontend/.env.local` for local development. Do not commit either file; `.env` is already ignored.
```

The tests cover important functionality such as:

* URL creation
* URL validation
* Short-code generation
* URL redirection
* Invalid short codes
* Database operations

---

# 🖥️ Example Usage

Suppose you want to shorten:

```text
https://www.example.com/articles/how-to-learn-fastapi
```

Send a request:

```http
POST /shorten
Content-Type: application/json
```

With:

```json
{
    "url": "https://www.example.com/articles/how-to-learn-fastapi"
}
```

The API may return:

```json
{
    "short_code": "x7Kp91",
    "short_url": "http://127.0.0.1:8000/x7Kp91"
}
```

Now instead of sharing the long URL, you can share:

```text
http://127.0.0.1:8000/x7Kp91
```

Opening the short URL automatically redirects the user to the original website.

---

# 📈 Future Improvements

The project can be extended with additional features:

* 👤 User authentication
* 🔑 API keys
* 📊 Advanced analytics dashboard
* 🌍 Custom domains
* ✏️ Custom short aliases
* ⏳ URL expiration
* 🗑️ URL deletion
* 📱 Frontend interface
* 🚦 Rate limiting
* ⚡ Redis caching
* 🐳 Docker support
* ☁️ Cloud deployment
* 🔒 Abuse and malicious URL detection
* 📈 Detailed click analytics
* 🌐 Custom branded short URLs

---

# 🔒 Security Considerations

A production-ready URL shortener should consider:

* Input validation
* Rate limiting
* Malicious URL detection
* Database query protection
* Abuse prevention
* Authentication for management APIs
* Protection against excessive URL creation
* Proper HTTP security headers

The current project is primarily intended for **learning and development purposes**.

---

# 🌐 Deployment

The application can be deployed using platforms that support Python/FastAPI applications.

A typical production command is:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

For production environments, additional configuration such as environment variables, a production database, HTTPS, logging, rate limiting, and reverse proxy configuration is recommended.

---

# 🎯 Learning Objectives

This project demonstrates practical concepts including:

* REST API development
* FastAPI
* HTTP methods
* URL redirection
* Database integration
* ORM concepts
* Data validation
* API documentation
* CRUD operations
* Unique identifier generation
* Backend project architecture
* Automated testing

---

# 🤝 Contributing

Contributions are welcome!

If you would like to improve the project:

1. Fork the repository
2. Create a new branch

```bash
git checkout -b feature/new-feature
```

3. Make your changes
4. Commit your changes

```bash
git commit -m "Add new feature"
```

5. Push the branch

```bash
git push origin feature/new-feature
```

6. Open a Pull Request

---

# 📄 License

This project is available under the **MIT License**.

---

## ⭐ Support

If you found this project useful, consider giving the repository a ⭐ on GitHub.

Built with Python 🐍 and FastAPI ⚡
