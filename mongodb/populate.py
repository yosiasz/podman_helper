import prestodb
conn=prestodb.dbapi.connect(
    host='localhost',
    port=8080,
    user='root',
    catalog='tpch',
    schema='sf1',
    #http_scheme='https',
    #auth=prestodb.auth.BasicAuthentication("root", ""),
)
cur = conn.cursor()
cur.execute('select *, now() from tpch.sf1.orders limit 10')
rows = cur.fetchall()