from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session
from app.core.config import SECRET_KEY, ALGORITHM
from app.db.session import get_session
from app.models.user import Usuario
from app.schemas.token import TokenData
from app.models.user import Usuario # CAMBIAR User por Usuario
from sqlmodel import select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

SessionDep = Annotated[Session, Depends(get_session)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]

def get_current_user(
    session: SessionDep,
    token: TokenDep
) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    # Buscar en la base de datos por el campo Usuario
    user = session.exec(select(Usuario).where(Usuario.Usuario == token_data.username)).first()
    if user is None:
        raise credentials_exception
    return user

CurrentUser = Annotated[Usuario, Depends(get_current_user)]