from fastapi import APIRouter

from app.api.endpoints import (
    test_router,
)

main_router = APIRouter()


main_router.include_router(
    test_router, prefix='/test', tags=['Test'])

# main_router.include_router(
#     user_router, prefix='/auth', tags=['Auth'])

# main_router.include_router(
#     template_router, prefix='/templates', tags=['templates'])

# main_router.include_router(
#     message_router, prefix='/send_message', tags=['message'])

# main_router.include_router(
#     send_setting_router, prefix='/sending_settings', tags=['settings'])
