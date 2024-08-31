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
        metrics.extract()

        if flag:
            metrics.transform()
            flag=False
        else:
            metrics.load()
            flag=True

            try:
                mynum = 3/0
            except Exception as e:
                metrics.error()

        heartbeat.send("UP", my_config, metrics)