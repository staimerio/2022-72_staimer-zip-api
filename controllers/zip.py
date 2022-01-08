# Retic
from retic import Request, Response, Next, App as app

# Services
from retic.services.responses import success_response, error_response
from retic.services.validations import validate_obligate_fields
from services.zip import zip
STORAGE_CREDENTIALS_DEFAULT = app.config.get('STORAGE_CREDENTIALS_DEFAULT')


def zip_images(req: Request, res: Response, next: Next):
    """Validate obligate params"""
    _validate = validate_obligate_fields({
        u'images_urls': req.param('images_urls'),
    })
    
    """Check if has errors return a error response"""
    if _validate["valid"] is False:
        return res.bad_request(
            error_response(
                "{} is necesary.".format(_validate["error"])
            )
        )
    
    storage_credential=req.headers.get('credential', STORAGE_CREDENTIALS_DEFAULT)
    """Get all novel from latests page"""
    _result = zip.zip_remote_images(
        images_url=req.param('images_url'),
        description_upload=req.param('description_upload', ""),
        credential=storage_credential,
        filename=req.param('filename', None),
    )
    """Check if exist an error"""
    if _result['valid'] is False:
        return res.bad_request(_result)
    """Response the data to client"""
    res.ok(_result)
