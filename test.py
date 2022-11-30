from Database import plates_db_api
db = plates_db_api()
x = db.query("9935QOX")
print(x)