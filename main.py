import time
import traceback

from app.heartbeat import MysqlHeartbeatManager, metrics


if __name__ == "__main__":

    heartbeat=MysqlHeartbeatManager(
        host="localhost",
        user="user",
        password="password",
        database="database",
        port=3306,
        table="table",
        servicename="myservice",
        interval=1
    )

    my_config = {
        "author": "myname",
        "repository": "http://github.com/{id}/{repository}"
    }

    flag=True
    while True:
        time.sleep(0.3)
        metrics.extract_cnt+=1

        if flag:
            metrics.transform_cnt+=1
            flag=False
        else:
            metrics.load_cnt+=1
            flag=True

            try:
                mynum = 3/0
            except Exception as e:
                metrics.error_cnt+=1

        heartbeat.send("UP", my_config, metrics)