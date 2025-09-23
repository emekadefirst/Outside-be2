from enum import Enum


class FileType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    DOCUMENT = "document"
    AUDIO = "audio"


class ImageExtension(str, Enum):
    JPG = "jpg"
    PNG = "png"
    JPEG = "jpeg"
    GIF = "gif"
    WEBP = "webp"
    BMP = "bmp"
    TIFF = "tiff"


class VideoExtension(str, Enum):
    MP4 = "mp4"
    AVI = "avi"
    MKV = "mkv"
    MOV = "mov"
    WMV = "wmv"
    FLV = "flv"
    WEBM = "webm"


class DocumentExtension(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    DOC = "doc"
    PPTX = "pptx"
    XLSX = "xlsx"
    TXT = "txt"
    ODT = "odt"
    RTF = "rtf"


class AudioExtension(str, Enum):
    MP3 = "mp3"
    WAV = "wav"
    AAC = "aac"
    FLAC = "flac"
    OGG = "ogg"
    WMA = "wma"
    M4A = "m4a"


class Action(str, Enum):
    READ = "read"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"



class Resource(str, Enum):
    FILE = "file"
    USER = "user"
    EVENT = "event"



class KYCDocType(str, Enum):
    NINC = "National Identity Card"
    DRIVER_LICENCE = "Driver's Licience"
    VOTER_CARD = "Voter's Card"
    PASSPORT = "Passport"
    SSN = "Social Security Number"

class KYCStatus(str, Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    DECLINE = "Declined"

class PaymentGateway(str, Enum):
    PAYSTACK = "Paystack"
    FLUTTERWAVE = "Flutterwave"
    STRIPE = "Stripe"

class PaymentStatus(str, Enum):
    SUCCESS = "success"
    PENDING = "pending"
    CANCELLED = "cancelled"
    FAILED = "failed"

class PaymentType(str, Enum):
    CRYTO = "crypto"
    CASH = "cash"


class AppModule(str, Enum):
    USER = "User"
    HOST = "Host"
    EVENT = "Event"
    SALE = "Sales"
    PAYOUT = "Payout"
    PERMISSION = "permission"