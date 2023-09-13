## Example of datetime field
CREATE TABLE log
(
	id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	timestamp DATETIME NOT NULL,
	user INT UNSIGNED,
	# ip BINARY(16) NOT NULL,
	action VARCHAR(20) NOT NULL,
	PRIMARY KEY (id, timestamp)
)
	ENGINE = InnoDB
PARTITION BY RANGE (YEAR(timestamp))
(
	PARTITION p0 VALUES LESS THAN (2013),
	PARTITION p1 VALUES LESS THAN (2014),
	PARTITION p2 VALUES LESS THAN (2015),
	PARTITION p3 VALUES LESS THAN (2016)
);


# This is insert for `timestamp` column of type `datetime`
INSERT INTO log(id,timestamp) VALUES
  (1, '2016-01-01'),
  (2, '2015-01-01');

  ## Example of timestamp field
CREATE TABLE log
(
	id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	timestamp TIMESTAMP NOT NULL,
	user INT UNSIGNED,
	ip BINARY(16) NOT NULL,
	action VARCHAR(20) NOT NULL,
	PRIMARY KEY (id, timestamp)
)
	ENGINE = InnoDB
PARTITION BY RANGE (UNIX_TIMESTAMP(timestamp))
(
	PARTITION p0 VALUES LESS THAN (UNIX_TIMESTAMP('2014-08-01 00:00:00')),
	PARTITION p1 VALUES LESS THAN (UNIX_TIMESTAMP('2014-11-01 00:00:00')),
	PARTITION p2 VALUES LESS THAN (UNIX_TIMESTAMP('2015-01-01 00:00:00')),
	PARTITION p3 VALUES LESS THAN (UNIX_TIMESTAMP('2015-02-01 00:00:00'))
);
# This is insert for `timestamp` column of type `timestamp`
INSERT INTO log(id,timestamp) VALUES
  (1, '2016-01-01 01:01:01'),
  (2, '2015-01-01 01:01:01');
