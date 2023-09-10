from flask import *
import pymysql,sqlite3


def get_mysql_attr(table_name,host,user,password,db):

    # Connect to the database
    connection = pymysql.connect(host=host, user=user, password=password, database=db)

    # Create a cursor
    cursor = connection.cursor()

    # Execute the query to get column names
    table_name = table_name
    query = f"DESCRIBE {table_name}"
    cursor.execute(query)

    # Fetch all the rows (column descriptions)
    columns_info = cursor.fetchall()

    # Extract column names from the fetched data
    column_names = [column_info[0] for column_info in columns_info]

    # Print the column names
    return column_names

    # Don't forget to close the cursor and connection when you're done
    cursor.close()
    connection.close()




def sqlitetable_attrs(table):
    conn = sqlite3.connect("static/db/database.db")
    cursor = conn.cursor()
    table_name = table
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    attrs = []
    for column in columns:
        attrs.append(column[1])
    
    conn.close()
    return attrs




app = Flask(__name__)
app.secret_key = "ksdfsefuh"
@app.route("/")
def homePage():
    return render_template("home.html")

@app.route("/sqlite")
def sqlLite():
    return render_template("sqlite.html")

@app.route("/mysql")
def mySQL():
    return render_template("mysql.html")

@app.route("/saveinfo",methods=["POST"])
def saveMYSQL():
    host = request.form['host']
    user = request.form['user']
    pwd = request.form['pass']
    database = request.form['database']
    dbinfo = {
        "host" : host,
        "user" : user,
        "password" : pwd,
        "db" : database
    }
    session['db-info'] = dbinfo
    return redirect("/loadmysql")


@app.route("/loadmysql")
def mysqlIde():
    host = session['db-info']['host']
    user = session['db-info']['user']
    pwd = session['db-info']['password']
    database = session['db-info']['db']
    try:
        with pymysql.connect(host=host,user=user,password=pwd,database=database) as conn:
            cur = conn.cursor()
            cur.execute("SHOW TABLES")
            tables = cur.fetchall()
        tables = [i[0] for i in tables]
        return render_template("mysql_ide.html",tables=tables)
    except Exception as e:
        print(e)
        flash(f"Error occured while connecting to database \n{e}",'error')
        return redirect("/mysql")

@app.route("/confirm",methods = ['POST'])
def red():
    dbfile = request.files['db']
    dbfile.save("static/db/database.db")
    return redirect("/loadsqlite")

@app.route("/loadsqlite")
def loadSQLite():
    with sqlite3.connect("static/db/database.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()
    tables = [i[0] for i in tables]
    return render_template("sqlite3_ide.html",tables=tables)

@app.route("/runsql",methods=["POST"])
def runSql():
    data = request.get_json()
    sqlquery = data['query']
    database= "static/db/database.db"
    try:
        with sqlite3.connect(database) as conn:
            cur = conn.cursor()
            cur.execute(sqlquery)
            outputs = cur.fetchall()
        return jsonify({"outputs" : outputs})
    except Exception as e:
        return jsonify({"error" : str(e)})
    
@app.route("/runmysql",methods=["POST"])
def runMySql():
    data = request.get_json()
    sqlquery = data['query']
    try:
        with pymysql.connect(host=session['db-info']['host'],user=session['db-info']['user'],password=session['db-info']['password'],database=session['db-info']['db']) as conn:
            cur = conn.cursor()
            cur.execute(sqlquery)
            outputs = cur.fetchall()
        return jsonify({"outputs" : list(outputs)})
    except Exception as e:
        return jsonify({"error" : str(e)})

@app.route("/getmysqlattr/<tablename>")
def getAttr(tablename):
    attrs = get_mysql_attr(tablename,session['db-info']['host'],session['db-info']['user'],session['db-info']['password'],session['db-info']['db'])
    return jsonify({"attributes" : attrs})

@app.route("/getsqlite3attrs/<table>")
def getsqliteattr(table):
    attrlist = sqlitetable_attrs(table)
    print(attrlist)
    return jsonify({"attributes" : attrlist})

if __name__ == '__main__':
    app.run(debug=True,port="4000")