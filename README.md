### mysql-heartbeat-python
```text
description
```
### DDL Guide
* mariadb-11.3.2
```sql
CREATE TABLE `heartbeat_table` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `servicename` varchar(255) NOT NULL,
  `instance` varchar(255) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `status` varchar(50) DEFAULT NULL,
  `config_json` text DEFAULT NULL,
  `raw_metrics` text DEFAULT NULL,
  `interval` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `heartbeat_table_servicename_IDX` (`servicename`,`instance`,`timestamp`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
```
