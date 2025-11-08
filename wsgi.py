from sacco_app import create_app

# Call your factory function to create the Flask app
app = create_app()

if __name__ == "__main__":
    app.run()
