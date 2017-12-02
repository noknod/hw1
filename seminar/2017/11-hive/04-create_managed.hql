USE agorokhov;

ADD JAR /opt/cloudera/parcels/CDH-5.9.0-1.cdh5.9.0.p0.23/lib/hive/lib/hive-contrib.jar;

DROP TABLE parsed_log;

CREATE TABLE parsed_log (
    ip STRING,
    date TIMESTAMP,
    status SMALLINT,
    url STRING,
    referer STRING
)
PARTITIONED BY (day string)
CLUSTERED BY (ip) SORTED BY (ip) INTO 8 BUCKETS
STORED AS TEXTFILE;

INSERT OVERWRITE TABLE parsed_log
PARTITION(day='2017-11-01')
SELECT
    ip,
    from_unixtime(unix_timestamp(date ,'dd/MMM/yyyy:HH:mm:ss')),
    CAST(status AS smallint),
    url,
    referer
FROM access_log
WHERE day='2017-11-01';

SHOW PARTITIONS parsed_log;
