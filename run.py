try:
    from app import app
except ImportError as e:
    print(f"Failed to import app: {e}")
    exit(1)

if __name__ == '__main__':
    # Use environment variables or configuration for these values
    # Default to development settings if not specified
    import os
    
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    
    app.run(
        host=host,
        port=port,
        debug=debug_mode
    )
