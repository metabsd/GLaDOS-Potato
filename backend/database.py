import MySQLdb

db = MySQLdb.connect("db", "root", "my-secret-pw", "bd_notes")

cursor = db.cursor()
global resultsExportEtudiants
resultsExportEtudiants = []

def getetudiants():
    del resultsExportEtudiants[:]
    sql = "SELECT * FROM t_etudiant"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            item = {
                "id_etudiant": row[0],
                "matricule": row[1],
                "prenom": row[2],
                "nom": row[3]
            }
            resultsExportEtudiants.append(item)
    except MySQLdb.Error as e:
        try:
            print ("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
            return None
        except IndexError:
            print ("MySQL Error: %s" % str(e))
            return None
        finally:
            cursor.close()
            db.close()


def createetudiant(etudiant):
    sql = "Insert into t_etudiant(matricule, nom, prenom) values('%s', '%s', '%s')" % (etudiant['matricule'], etudiant['nom'], etudiant['prenom'])
    try:
        cursor.execute(sql)
        db.commit()
    except MySQLdb.Error as e:
        try:
            print ("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
            return None
        except IndexError:
            db.rollback()
            print ("MySQL Error: %s" % str(e))
            return None
        finally:
            cursor.close()
            db.close()
