from pymongo import MongoClient


class DB_Connection:
    def db_connect():
        client = MongoClient(
            host="mongodb://datahub:echoss2021!@8q7bd.pub-vpc.mg.naverncp.com:17017/echoss_raw_db?authMechanism=DEFAULT&directConnection=true"
        )

        ## DB 선택
        db = client["echoss_raw_db"]  ## collection 조회
        db.list_collection_names()
        return db
