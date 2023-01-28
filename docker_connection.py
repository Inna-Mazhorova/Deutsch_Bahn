# create sqlalchemy engine

engine = create_engine("mysql+pymysql://{user}:{pw}@127.0.0.1/{db}"
                       .format(user="Lantana",
                               pw="db1234567!",
                               db="deutsche_bahn"))

# Insert whole DataFrame into MySQL
df.to_sql('stations', con = engine, if_exists = 'append', chunksize = 1000)

# create connection
connection = pymysql.connect(host='8080',
                             user='root',
                             password='12345',
                             db='deutsche_bahn')

# Create cursor
my_cursor = connection.cursor()

# Execute Query
my_cursor.execute("SELECT * from deutsche_bahn")

# Fetch the records
result = my_cursor.fetchall()

for i in result:
    print(i)

# Close the connection
connection.close()