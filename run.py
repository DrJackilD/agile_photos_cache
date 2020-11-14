from agile_photo_collection import settings
from agile_photo_collection.app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=settings.DEBUG)
