from app import create_app

# Create app instance for production (gunicorn)
app = create_app()

# For development testing
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
