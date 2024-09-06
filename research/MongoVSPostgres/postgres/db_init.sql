create user replicator with replication encrypted password 'replicator_password';
select pg_create_physical_replication_slot('replication_slot');

\c test_db

CREATE TABLE IF NOT EXISTS likes
(
	id uuid not null
		constraint likes_pk
			primary key,
	user_id uuid not null,
	liked_id uuid not null,
	rate smallint not null,
    datetime timestamp not null
);

ALTER TABLE likes owner TO "user_db";

CREATE INDEX IF NOT EXISTS likes_datetime_index
	ON likes (datetime);

CREATE TABLE IF NOT EXISTS reviews
(
	id uuid not null
		constraint reviews_pk
			primary key,
	user_id uuid not null,
	movie_id uuid not null,
	datetime timestamp not null,
	text text not null
);

ALTER TABLE reviews owner TO "user_db";

CREATE INDEX IF NOT EXISTS review_datetime_index
	ON reviews (datetime);


CREATE TABLE IF NOT EXISTS bookmarks
(
	id uuid not null
		constraint bookmarks_pk
			primary key,
	user_id uuid not null,
	movie_id uuid not null,
    datetime timestamp not null
);

ALTER TABLE bookmarks owner TO "user_db";

CREATE INDEX IF NOT EXISTS bookmark_datetime_index
	ON bookmarks (datetime);
