from pydantic import BaseModel


class MfaSetupResponse(BaseModel):
    secret: str
    provisioning_uri: str


class MfaVerifyRequest(BaseModel):
    code: str


class MessageResponse(BaseModel):
    detail: str
