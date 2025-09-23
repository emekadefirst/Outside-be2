from src.utilities.base_model import BaseModel
from tortoise import fields
from src.enums.base import KYCDocType, KYCStatus

class KYC(BaseModel):
    user = fields.ForeignKeyField("models.User", related_name="kyc_documents")
    type = fields.CharEnumField(KYCDocType)
    document_id = fields.CharField(15, unique=True)
    front_side = fields.ForeignKeyField('models.File', related_name="kyc_front_sides")
    back_side = fields.ForeignKeyField('models.File', related_name="kyc_back_sides")
    status = fields.CharEnumField(KYCStatus)
    
    class Meta:
        table = "kyc_documents"