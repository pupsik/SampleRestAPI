--liquibase formatted sql

--changeset rita.linets:1 labels:init context:will ignore FKs for simplicity
--comment: create original tables
create table postgres.public.tbl_pl_cancellation_policy (
    cancellation_policy_id int GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    cancellation_policy_name varchar(100)
);

create table postgres.public.tbl_pl_room_type (
    room_type_id int GENERATED BY DEFAULT as IDENTITY PRIMARY KEY,
    room_type_name varchar(100)
);

create table postgres.public.tbl_host (
    host_id BIGINT GENERATED BY DEFAULT as IDENTITY PRIMARY KEY,
    host_identity_verified boolean, 
    host_name varchar(100)
);

create table postgres.public.tbl_listings (
    id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    name varchar(250),
    host_id BIGINT REFERENCES tbl_host (host_id), 
    neighbourhood_group varchar(100),
    neighbourhood varchar(150),
    lat numeric, 
    long numeric,
    instant_bookable boolean, 
    cancellation_policy_id int REFERENCES tbl_pl_cancellation_policy (cancellation_policy_id), 
    room_type_id int REFERENCES tbl_pl_room_type (room_type_id), 
    construction_year int, 
    price int, 
    service_fee int, 
    minimum_nights int, 
    number_of_reviews int, 
    last_review date, 
    reviews_per_month float(2),
    review_rate_number int, 
    calculated_host_listings_count int,
    availability_365 int,
    house_rules text
);

create index tbl_listings_idx ON tbl_listings (room_type_id);

