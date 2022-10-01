from fastapi import APIRouter, Depends

from core.config import settings
from models.models import Template, StatusMessage
from services.doc_service import DocService
from services.service_locator import get_storage_service

router = APIRouter()


@router.post('/',
             response_model=StatusMessage,
             summary="Add template from database",
             description="Add template from database")
async def add_template(template: Template,
                       storage_service: DocService = Depends(get_storage_service)):
    db_record_id = await storage_service.insert(template, settings.MONGO_TEMPLATE_TABLE)

    return StatusMessage(status='OK', body=f'template was added with id={db_record_id}')


@router.get('/',
            response_model=list[Template],
            summary="Get template from database",
            description="Get template from database")
async def get_template(name: str,
                       transport: str,
                       storage_service: DocService = Depends(get_storage_service)):
    templates = await storage_service.select({'name': name, 'transport': transport}, settings.MONGO_TEMPLATE_TABLE)

    return [Template(**template) for template in templates]
