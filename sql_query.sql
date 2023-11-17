create table realtime_seoul (
	area varchar(100),
    time varchar(100),
    comment varchar(100),
    di varchar(40)
);

create table places(
	name varchar(255) primary key,
    latitude varchar(255),
    longitude varchar(255)
);

select * from realtime_seoul;
drop table realtime_seoul;

select * from crime_data;
drop table crime_data;

select * from places;
select count(*) from places where latitude=0;
drop table places;

alter table places add borough varchar(255) NULL;
alter table places add safe_score int NULL;

select name, crime_data.safe_score from crime_data, places where crime_data.area = places.borough;

SELECT name, latitude, longitude, borough, time, di, safe_score 
FROM realtime_seoul, places 
WHERE realtime_seoul.area = places.name;