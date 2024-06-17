from fastapi import APIRouter

router = APIRouter(
    tag = ['Login']
)

@router.post('/login')
def login():
    return 'login'