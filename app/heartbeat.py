import logging
import time
import socket
import json
from datetime import datetime, timezone, timedelta

import pymysql.cursors

logger = logging.getLogger(__name__)


class DefaultHeartbeatMetric():
    def __init__(self):
        self.startup_time=self.__get_kst_now()

        self.collected_from=self.__get_kst_now()
        self.extract_cnt=0
        self.transform_cnt=0
        self.load_cnt=0
        self.warnning_cnt=0
        self.error_cnt=0

    def reset(self):
        self.collected_from=self.__get_kst_now()
        self.extract_cnt=0
        self.transform_cnt=0
        self.load_cnt=0
        self.warnning_cnt=0
        self.error_cnt=0

    def __get_kst_now(self):
        kst_now = datetime.now(timezone.utc) + timedelta(hours=9)
        return kst_now.strftime('%Y-%m-%d %H:%M:%S')


class MysqlHeartbeatManager():
    def __init__(self, host:str, user:str, password:str, database:str, port:int, table:str, servicename:str, interval:float):
        self.host=host
        self.user=user
        self.password=password
        self.database=database
        self.port=port
        self.table=table
        
        self.servicename=servicename
        self.interval=interval
        self.interval_backup=interval
        self.send_time=time.time()

        self.connection=None

    def __get_connection(self):
        if self.connection:
            return self.connection
        
        try:
            connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                cursorclass=pymysql.cursors.DictCursor
            )

            if connection:
                self.connection=connection

            return self.connection
        except Exception as e:
            logger.error(f"Database connection fail:{e}")
            return None
        
    def send(self, status, config, metrics:DefaultHeartbeatMetric):
        try:
            if self.__is_timeover():
                
                #instance=self.__get_ip_address()
                instance=self.__get_hostname()
                config_json=self.__get_attr_json(config)
                metics_json=self.__get_attr_json(metrics)

                self.__insert_heartbeat(
                    instance=instance,
                    status=status,
                    config_json=config_json,
                    metric_json=metics_json
                )
                self.send_time=time.time()
                metrics.reset()
                self.interval=self.interval_backup
        except Exception as e:
            logger.error(f"Heartbeat fails:{e}")
            self.interval*=2
            

    def __insert_heartbeat(self, instance:str, status:str, config_json:str, metric_json:str):
        sql="INSERT INTO " + self.table + " (servicename, instance, interval_sec, status, config_json, raw_metrics) VALUES (%s, %s, %s, %s, %s, %s)"
        params=(self.servicename, instance, self.interval, status, config_json, metric_json)

        try:
            connection=self.__get_connection()

            if connection:
                connection.ping(reconnect=True)

                with connection.cursor() as cursor:
                    cursor.execute(sql, params)
                
                connection.commit()
        except Exception as e:
            logger.error(f"Insert exception:{e}")

    def __is_timeover(self) -> bool:
        return time.time() - self.send_time > self.interval
    
    def __get_ip_address(self) -> str:
        try:
            hostname=socket.gethostname()
            ip_address=socket.gethostbyname(hostname)
            return ip_address
        except Exception as e:
            return "ip_error"
        
    def __get_hostname(self) -> str:
        try:
            return socket.gethostname()
        except Exception as e:
            return "hostname_error"
        
    def __get_attr_json(self, instance) -> dict:
        if isinstance(instance, dict):
            return json.dumps(instance)
        elif isinstance(instance, object) and hasattr(instance, "__dict__"):
            return json.dumps(instance.__dict__)

        if instance:    
            return json.dumps({"config": instance.__class__.__name__})
        
        return json.dumps({"config": None})

metrics = DefaultHeartbeatMetric()