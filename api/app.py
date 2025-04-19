from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, ValidationError, EmailStr

from keycloak import KeycloakError, KeycloakOpenID

import os

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

keycloak_openid = KeycloakOpenID(
    server_url = os.environ.get("FASTAPI_APP_KEYCLOAK_URL", "http://localhost:8080"),
    client_id = os.environ.get("FASTAPI_APP_KEYCLOAK_CLIENT_ID", "reports-backend"),
    realm_name = os.environ.get("FASTAPI_APP_KEYCLOAK_REALM", "reports-realm"),
)

class RealmAccess(BaseModel):
    roles: list[str]

class KeycloackUserInfo(BaseModel, extra='allow'):
    realm_access: RealmAccess
    name: str
    preferred_username: str
    given_name: str
    family_name: str
    email: EmailStr

def get_payload_if_authorized(token: str = Depends(oauth2_scheme)):
    try:
        payload = keycloak_openid.decode_token(token)

    except (ValidationError, KeycloakError):
        raise HTTPException(status_code=401, detail="Unauthorized")

    return payload


@app.get("/reports")
def read_reports(payload: dict = Depends(get_payload_if_authorized)):

    keycloak_user_info = KeycloackUserInfo.model_validate(payload)

    if "prothetic_user" not in keycloak_user_info.realm_access.roles:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Произвольные данные
    return {"current_user": keycloak_user_info.model_dump()}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)