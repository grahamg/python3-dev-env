# python3-dev-env

A container-based Python back-end environment featuring:

- **Flask** web application using **MySQL** for data storage  
- **ngrok** to publicly expose the app  
- A **dev environment** container with LunarVim, Python dev tools, Node.js LTS, Git, Jupyter, etc.  
- **Makefile** for quick, common operations  
- **Invoke** (`tasks.py`) for Pythonic command-running  
- **docker-compose** override files for **development**, **production**, and **staging**  
- **pytest** for tests  
- **pipenv** for optional dependency management

---

## Project Structure

```
my_todo_app/
├── docker-compose.yml                # Base Docker Compose file
├── docker-compose.dev.yml            # Development overrides
├── docker-compose.prod.yml           # Production overrides
├── docker-compose.staging.yml        # Staging overrides
├── Makefile                          # Make-based command shortcuts
├── Pipfile                           # pipenv dependencies (optional)
├── Pipfile.lock                      # Generated pipenv lock file
├── README.md                         # This README
├── tasks.py                          # Invoke tasks
├── flask_app/
│   ├── app.py                        # Flask app code
│   ├── requirements.txt              # Traditional requirements file (if not using pipenv)
│   └── Dockerfile                    # Docker build for Flask
├── dev_env/
│   └── Dockerfile                    # Docker build for dev environment
├── ngrok/
│   └── Dockerfile                    # Docker build for ngrok
└── tests/
    └── test_app.py                   # Sample pytest tests
```

---

## Quick Start

1. **Clone** this repository:
   ```bash
   git clone https://github.com/grahamg/python3-dev-env.git
   cd python3-dev-env
   ```

2. **(Optional) Install pipenv** if you want advanced Python dependency management:
   ```bash
   pip install pipenv
   ```
   or rely on the standard `requirements.txt`.

3. **Build and run** in development mode:
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build
   ```
   Alternatively, you can use the **Makefile** or **Invoke** tasks (see below).

4. **View the Flask App**:  
   - In your browser, go to [http://localhost:8003](http://localhost:8003).  
   - You should see the to-do list interface.

5. **Check ngrok**:  
   - The public URL can be found in the container logs or the local ngrok dashboard at [http://localhost:4040](http://localhost:4040).

6. **Stop** the environment:
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml down
   ```
   or use the **Makefile** / **Invoke** commands.

---

## Docker Compose Overrides

We use multiple files to separate configuration:

- **`docker-compose.yml`**: Base configuration (Flask, MySQL, dev_env, ngrok).  
- **`docker-compose.dev.yml`**: Development overrides (e.g., volume mounts, environment variables, etc.).  
- **`docker-compose.prod.yml`**: Production overrides (remove local volumes, set `FLASK_ENV=production`, etc.).  
- **`docker-compose.staging.yml`**: Staging overrides (similar to production, but with staging environment vars).

### Usage Examples

- **Development**:
  ```bash
  docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build
  ```
- **Production**:
  ```bash
  docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build
  ```
- **Staging**:
  ```bash
  docker-compose -f docker-compose.yml -f docker-compose.staging.yml up --build
  ```

---

## Makefile Usage

A `Makefile` provides convenient shortcuts for common operations. Example targets:

- **`make build`** – Builds all containers.  
- **`make up`** – Brings up all services (in dev mode).  
- **`make down`** – Stops all services (in dev mode).  
- **`make test`** – Runs `pytest` inside the dev container.  
- **`make shell`** – Opens a bash shell in the dev container.

### Example

```bash
# Build all images
make build

# Run in dev mode (detached)
make up

# Run tests
make test

# Stop everything
make down
```

You can customize the Makefile rules as needed.

---

## Invoke (tasks.py)

We also include a Python-based task runner using **Invoke**. See `tasks.py` for definitions like:

- `inv build`  
- `inv up [--env=dev|prod|staging]`  
- `inv down [--env=dev|prod|staging]`  
- `inv test`  
- `inv shell`

### Example

```bash
# Install invoke if needed
pip install invoke

# Build the images
inv build

# Bring up dev environment
inv up

# Bring down dev environment
inv down

# Run tests in dev_env container
inv test
```

By default, `env=dev`. You can override with `--env=prod` or `--env=staging`.

---

## The Dev Environment Container

- Based on `ubuntu:22.04`
- Includes:
  - Python 3, pip, pipenv, build-essential
  - Node.js + npm
  - Jupyter Notebook
  - LunarVim, Emacs, nano, tig, netcat
  - Git, etc.

To **develop** inside this container:

1. Ensure containers are running:
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d dev_env
   ```
2. **Shell** in:
   ```bash
   docker exec -it dev_env /bin/bash
   ```
3. Your project files are typically in `/workspace` (based on the `docker-compose.yml` volume mount).

Inside, you can run:
- `lvim` or `emacs` or `nano` to edit files.  
- `pipenv install` or `pip install` to manage dependencies.  
- `pytest` to run tests (or `make test` / `inv test` from the host).  

---

## The Flask App

Located in `flask_app/`.  
- **`app.py`**: Basic Flask to-do application.  
- Connects to MySQL using environment variables:  
  - `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`  
- Exposes HTTP on port `8003`.

### Example Endpoints

- `GET /` – Show the to-do list (HTML).  
- `POST /add` – Add a new task (`form-data` key: `task`).  
- `POST /complete/<int:task_id>` – Mark a task as completed.

---

## The MySQL Container

- Using official `mysql:8.0` image.  
- Root password = `root` (development only!).  
- Database = `todo_db`.  
- Mapped port is `3306` on the host (if you need direct DB access).

---

## ngrok Container

- Based on a minimal Alpine image.  
- Exposes the Flask app publicly at a random subdomain.  
- Internal command: `ngrok http flask_app:8003`.  
- Access the ngrok web interface at [http://localhost:4040](http://localhost:4040).

---

## Testing with pytest

We have a `tests/` directory containing sample tests (e.g., `test_app.py`).

- **Install** `pytest` (already in `Pipfile` or `requirements.txt`).  
- Ensure containers are running (especially `flask_app`).  
- **Run** from the host machine via dev_env:
  ```bash
  docker exec -it dev_env pytest
  ```
  or with the Makefile:
  ```bash
  make test
  ```
  or with Invoke:
  ```bash
  inv test
  ```
  or directly from inside `dev_env`:
  ```bash
  pytest
  ```

---

## pipenv

If you prefer **pipenv** over `requirements.txt`:

1. **Check** `Pipfile` in the project root, containing dependencies like `Flask`, `mysql-connector-python`, `pytest`, `invoke`, etc.  
2. In the dev container:
   ```bash
   cd /workspace
   pipenv install
   ```
3. **Run** your Flask app under pipenv:
   ```bash
   pipenv run python flask_app/app.py
   ```
4. Or just rely on `requirements.txt` within the `flask_app` Docker build.  

*(Both approaches are valid; choose whichever you prefer.)*

---

## Contributing

- **Issues** and **pull requests** are welcome.  
- For major changes, please open an issue first.  
- Adhere to coding standards and test thoroughly.

---

## License

This project is provided under an open-source license (e.g., MIT).  
Feel free to modify, distribute, or adapt as needed.  

---

## Additional Notes & Suggestions

1. **Linting/Formatting**: Tools like **Black**, **flake8**, or **isort** can be installed to keep code consistent.  
2. **Continuous Integration**: If you use GitHub or GitLab, set up a CI pipeline to run `pytest` on every push.  
3. **Secrets Management**: For production, do **not** store passwords (like root) in plain text. Consider using Docker secrets, environment variable management, or a vault.  
4. **Production Hardening**: Instead of the built-in Flask server, consider `gunicorn` or `uwsgi` behind a reverse proxy.  
5. **Scaling**: For heavier usage, adopt container orchestration (Kubernetes, ECS, etc.) or at least scale MySQL with persistent volumes.  

---

**Enjoy building and deploying your Python Flask to-do application with a robust, Docker-based dev environment!**
