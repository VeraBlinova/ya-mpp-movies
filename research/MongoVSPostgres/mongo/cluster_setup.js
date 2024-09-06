sh.addShard("mongo_rs1/mongo_n1:27017,mongo_n2:27017")

sh.enableSharding("test_db")
db.createCollection("test_db.reviews")
db.createCollection("test_db.bookmarks")
db.createCollection("test_db.likes")
sh.shardCollection("test_db.reviews", {"datetime" : "hashed"})
sh.shardCollection("test_db.bookmarks", {"datetime": "hashed"})
sh.shardCollection("test_db.likes", {"datetime": "hashed"})
