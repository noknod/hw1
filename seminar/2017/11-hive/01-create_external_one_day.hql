USE agorokhov;

DROP TABLE access_log_20171101;
CREATE EXTERNAL TABLE access_log_20171101 (
    ip STRING,
    date STRING,
    url STRING,
    status STRING,
    referer STRING,
    user_agent STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.contrib.serde2.RegexSerDe'
WITH SERDEPROPERTIES (
    "input.regex" = "([\\d\\.:]+) - - \\[(\\S+) [^\"]+\\] \"\\w+ ([^\"]+) HTTP/[\\d\\.]+\" (\\d+) \\d+ \"([^\"]+)\" \"(.*?)\""
)
STORED AS TEXTFILE
LOCATION '/user/bigdatashad/logs/2017-11-01';


SELECT * FROM access_log_20171101 LIMIT 10;


SELECT ip FROM access_log_20171101
WHERE status = '200'
LIMIT 10;

