-- Adminer 4.8.1 PostgreSQL 15.3 dump

--connect "grafana";

DROP TABLE IF EXISTS "posts";
CREATE TABLE "public"."posts" (
    "title" text NOT NULL,
    "content" integer NOT NULL,
    "published" boolean NOT NULL,
    "created_at" timestamptz NOT NULL
) WITH (oids = false);

TRUNCATE "posts";
INSERT INTO "posts" ("title", "content", "published", "created_at") VALUES
('Hello',	1,	't',	'2023-05-24 16:23:46.73799+00');



DROP TABLE IF EXISTS "devices";
CREATE TABLE "public"."devices" (
    "device" text NOT NULL,
    "registered_date" timestamptz NOT NULL
) WITH (oids = false);

TRUNCATE "devices";
INSERT INTO "devices" ("device", "registered_date") VALUES
('WHITELISTED',	'2023-06-07 08:23:46.73799+00'),
('WHITELISTED',	'2023-06-07 10:23:46.73799+00'),
('ZOOMZAM',	'2023-06-07 10:23:46.73799+00'),
('WHITELISTED',	'2023-06-07 16:23:46.73799+00');

-- 2023-05-25 14:46:01.288843+00
