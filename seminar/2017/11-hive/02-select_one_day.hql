USE agorokhov;
ADD JAR /opt/cloudera/parcels/CDH-5.9.0-1.cdh5.9.0.p0.23/lib/hive/lib/hive-contrib.jar;

SELECT ip FROM access_log_20171101
WHERE status = '200'
LIMIT 10;

