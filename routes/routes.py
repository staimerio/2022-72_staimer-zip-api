# Retic
from retic import Router

# Controllers
import controllers.zip as zip

router = Router()

router.post("/zip-images", zip.zip_images)
