# Django PostgreSQL Project

A Django application configured to work with PostgreSQL (including cloud databases like Neon).

## Prerequisites

- Python 3.8 or higher
- PostgreSQL database (local or cloud-based like Neon)

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd demo-transaction
```

### 2. Create and activate a virtual environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example environment file and update with your database credentials:

```bash
cp .env.example .env
```

Edit `.env` and update the DATABASE_URL with your PostgreSQL connection string:

```
DATABASE_URL=postgresql://username:password@host:port/database?sslmode=require
```

For Neon database, use the connection string from your Neon dashboard.

### 5. Run database migrations

```bash
python manage.py migrate
```

### 6. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Project Structure

```
demo-transaction/
├── backend/          # Django project settings
├── manage.py         # Django management script
├── requirements.txt  # Python dependencies
├── .env             # Environment variables (not in git)
├── .env.example     # Example environment variables
└── .gitignore       # Git ignore file
```

## Environment Variables

The project uses the following environment variables:

- `DATABASE_URL`: PostgreSQL connection string (preferred method)
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)

Alternative database configuration (if not using DATABASE_URL):
- `DB_NAME`: Database name
- `DB_USER`: Database user
- `DB_PASSWORD`: Database password
- `DB_HOST`: Database host
- `DB_PORT`: Database port (default: 5432)

## Troubleshooting

### Database Connection Issues

If you encounter connection errors:

1. Verify your database credentials in `.env`
2. Ensure your PostgreSQL server is running
3. Check that your IP is whitelisted (for cloud databases)
4. Verify SSL settings match your database configuration

### Missing Dependencies

If you get import errors, ensure all packages are installed:

```bash
pip install --upgrade -r requirements.txt
```

## Development

To deactivate the virtual environment when done:

```bash
deactivate
```