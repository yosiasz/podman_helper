-- Adminer 4.8.1 PostgreSQL 15.3 dump

\connect "grafana";

DROP TABLE IF EXISTS "posts";
CREATE TABLE "public"."posts" (
    "title" character varying(25) NOT NULL,
    "content" character varying(25) NOT NULL,
    "isPublished" boolean NOT NULL,
    "createdAt" timestamptz NOT NULL
) WITH (oids = false);

TRUNCATE "posts";
INSERT INTO "posts" ("title", "content", "isPublished", "createdAt") VALUES
('wewe',	'wewew',	't',	'2023-05-25 05:29:36.452767+00');

-- 2023-05-25 05:31:06.61834+00