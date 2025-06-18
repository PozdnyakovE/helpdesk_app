from fastapi import APIRouter
# from sqlalchemy.ext.asyncio import AsyncSession


# from app.core.database import get_async_session

router = APIRouter()


@router.get(
    '/test_endpoint',
)
async def get_all_templates():
    """Testing endpoint."""
    return {'msg': 'Hello world!'}
