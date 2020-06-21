#%%

# EXECUTE QUERIES AND CLOSE PYTHON CONNECTION

def execute_queries(conn, queries):
    cur = conn.cursor()

    # Execute Drop Table Queries
    for query_set in queries:
        for query in query_set:
            try:
                print(query)
                cur.execute(query)
                conn.commit()
            except Exception as e:
                cur.execute('rollback;')
                print(e)
                break

#%%
