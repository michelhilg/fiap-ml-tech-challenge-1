from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os

router = APIRouter()

# Configuração do JWT
SECRET_KEY = os.getenv("JWT_SECRET", "supersecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Usuário e senha fixos (pode integrar com banco futuramente)
FAKE_USER = {
    "username": "admin",
    "password": "admin123"
}

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Token inválido ou não fornecido",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username != FAKE_USER["username"]:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if (form_data.username != FAKE_USER["username"] or 
        form_data.password != FAKE_USER["password"]):
        raise HTTPException(status_code=400, detail="Usuário ou senha inválidos")
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh")
def refresh_token(authorization: str = Header(...)):
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        new_access_token = create_access_token({"sub": username})
        return {"access_token": new_access_token, "token_type": "bearer"}
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
