from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "permissions" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "action" VARCHAR(6) NOT NULL,
    "module" VARCHAR(100) NOT NULL
);
COMMENT ON COLUMN "permissions"."action" IS 'READ: read\nWRITE: write\nUPDATE: update\nDELETE: delete';
CREATE TABLE IF NOT EXISTS "permission_groups" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "name" VARCHAR(100) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "users" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "first_name" VARCHAR(55),
    "last_name" VARCHAR(55),
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "phone_number" VARCHAR(20) NOT NULL UNIQUE,
    "is_superuser" BOOL NOT NULL DEFAULT False,
    "is_staff" BOOL NOT NULL DEFAULT False,
    "is_host" BOOL NOT NULL DEFAULT False,
    "is_verified" BOOL NOT NULL DEFAULT False,
    "password" VARCHAR(128)
);
CREATE TABLE IF NOT EXISTS "files" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "name" VARCHAR(150) NOT NULL,
    "slug" VARCHAR(250) NOT NULL UNIQUE,
    "type" VARCHAR(8) NOT NULL,
    "extension" VARCHAR(10),
    "mime_type" VARCHAR(100),
    "url" VARCHAR(500) NOT NULL,
    "size" BIGINT NOT NULL,
    "width" INT,
    "height" INT,
    "duration" DOUBLE PRECISION,
    "is_public" BOOL NOT NULL DEFAULT True,
    "is_active" BOOL NOT NULL DEFAULT True,
    "user_id" UUID REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_files_slug_1c60f3" ON "files" ("slug");
COMMENT ON COLUMN "files"."type" IS 'IMAGE: image\nVIDEO: video\nDOCUMENT: document\nAUDIO: audio';
CREATE TABLE IF NOT EXISTS "events" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "title" VARCHAR(155) NOT NULL UNIQUE,
    "description" TEXT,
    "time" JSONB NOT NULL,
    "latitude" DOUBLE PRECISION,
    "longitude" DOUBLE PRECISION,
    "address" VARCHAR(500) NOT NULL,
    "banner_id" UUID REFERENCES "files" ("id") ON DELETE SET NULL,
    "host_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "kyc_documents" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "type" VARCHAR(22) NOT NULL,
    "document_id" VARCHAR(15) NOT NULL UNIQUE,
    "status" VARCHAR(8) NOT NULL,
    "back_side_id" UUID NOT NULL REFERENCES "files" ("id") ON DELETE CASCADE,
    "front_side_id" UUID NOT NULL REFERENCES "files" ("id") ON DELETE CASCADE,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "kyc_documents"."type" IS 'NINC: National Identity Card\nDRIVER_LICENCE: Driver''s Licience\nVOTER_CARD: Voter''s Card\nPASSPORT: Passport\nSSN: Social Security Number';
COMMENT ON COLUMN "kyc_documents"."status" IS 'PENDING: Pending\nAPPROVED: Approved\nDECLINE: Declined';
CREATE TABLE IF NOT EXISTS "payouts" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "total" DECIMAL(12,2) NOT NULL,
    "paid_at" TIMESTAMPTZ,
    "status" VARCHAR(9) NOT NULL DEFAULT 'pending',
    "payment_ref_id" VARCHAR(255) UNIQUE,
    "event_id" UUID NOT NULL REFERENCES "events" ("id") ON DELETE CASCADE,
    "host_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "payouts"."status" IS 'SUCCESS: success\nPENDING: pending\nCANCELLED: cancelled\nFAILED: failed';
CREATE TABLE IF NOT EXISTS "tickets" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "name" VARCHAR(55) NOT NULL,
    "cost" DECIMAL(10,2) NOT NULL,
    "quantity" INT NOT NULL,
    "event_id" UUID NOT NULL REFERENCES "events" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "payins" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "provider" VARCHAR(11) NOT NULL,
    "quantity" INT NOT NULL,
    "total_cost" DECIMAL(10,2) NOT NULL,
    "status" VARCHAR(9) NOT NULL DEFAULT 'pending',
    "payment_ref_id" VARCHAR(255) UNIQUE,
    "email" VARCHAR(255),
    "fullname" VARCHAR(255),
    "phone_number" VARCHAR(20),
    "payment_type" VARCHAR(6) NOT NULL DEFAULT 'cash',
    "paid_at" TIMESTAMPTZ,
    "ticket_id" UUID NOT NULL REFERENCES "tickets" ("id") ON DELETE CASCADE,
    "user_id" UUID REFERENCES "users" ("id") ON DELETE SET NULL
);
COMMENT ON COLUMN "payins"."provider" IS 'PAYSTACK: Paystack\nFLUTTERWAVE: Flutterwave\nSTRIPE: Stripe';
COMMENT ON COLUMN "payins"."status" IS 'SUCCESS: success\nPENDING: pending\nCANCELLED: cancelled\nFAILED: failed';
COMMENT ON COLUMN "payins"."payment_type" IS 'CRYTO: crypto\nCASH: cash';
CREATE TABLE IF NOT EXISTS "orders" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "serial_number" VARCHAR(50) NOT NULL UNIQUE,
    "issued_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "delivery_mail" JSONB,
    "payment_id" UUID NOT NULL REFERENCES "payins" ("id") ON DELETE CASCADE,
    "ticket_id" UUID NOT NULL REFERENCES "tickets" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "permission_groups_permissions" (
    "permission_groups_id" UUID NOT NULL REFERENCES "permission_groups" ("id") ON DELETE CASCADE,
    "permission_id" UUID NOT NULL REFERENCES "permissions" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_permission__permiss_4949c5" ON "permission_groups_permissions" ("permission_groups_id", "permission_id");
CREATE TABLE IF NOT EXISTS "users_permission_groups" (
    "users_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "permissiongroup_id" UUID NOT NULL REFERENCES "permission_groups" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_users_permi_users_i_9954a4" ON "users_permission_groups" ("users_id", "permissiongroup_id");
CREATE TABLE IF NOT EXISTS "events_files" (
    "events_id" UUID NOT NULL REFERENCES "events" ("id") ON DELETE CASCADE,
    "file_id" UUID NOT NULL REFERENCES "files" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_events_file_events__67c994" ON "events_files" ("events_id", "file_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
