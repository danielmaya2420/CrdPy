import pymysql
import csv


class Data:
    def __init__(self):
        self.conn = pymysql.connect(
            host="localhost", user="root", password="", db="prueba"
        )

        self.cursor = self.conn.cursor()

    def InsertItems(self, element):
        # our element contend the name, age and the carreer of the student
        # in position 0, 1, 2
        sql = "insert into persona(edad, entubado, neumonia) values('{}', '{}', '{}')".format(
            element[0], element[1], element[2]
        )
        # execute the query
        self.cursor.execute(sql)
        self.conn.commit()  # guardamos cambios

    def ReturnOneItem(self, ref):
        # we have ref like name of the element
        sql = "select * from persona where ed = '{}'".format(ref)
        self.cursor.execute(sql)
        # return the element or nil
        return self.cursor.fetchone()

    def returnAllElements(self):
        sql = "select * from persona"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def Delete(self, ref):
        sql = "delete from persona where edad = '{}'".format(ref)
        self.cursor.execute(sql)
        self.conn.commit()

    def UpdateItem(self, element, ref):
        # element contains the values and ref is the name of the item that we want change
        sql = "update persona set edad = '{}',entubado = '{}', neumonia='{}' where edad = '{}'".format(
            element[0], element[1], element[2], ref
        )
        # execute the query
        self.cursor.execute(sql)
        self.conn.commit()  # guardamos cambios

    def exportData(self, filename):
        if not filename.lower().endswith(".csv"):
            filename = filename + ".csv"

        rows = self.returnAllElements()
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["edad", "entubado", "neumonia"])  # header row
            writer.writerows(rows)

    def importData(self, filename):
        try:
            with open(filename, "r") as csvfile:
                csv_reader = csv.DictReader(csvfile)
                successful_inserts = 0
                total_rows = 0

                for row in csv_reader:
                    total_rows += 1
                    edad = row.get("edad", "")
                    entubado = row.get("entubado", "")
                    neumonia = row.get("neumonia", "")

                    if edad and entubado and neumonia:
                        if self.InsertItems([edad, entubado, neumonia]):
                            successful_inserts += 1
                            print(f"Datos de {edad} insertados correctamente.")
                        else:
                            print(f"Error al insertar datos de {edad}.")
                    else:
                        print(
                            f"Error en la fila {total_rows}: Datos incompletos o faltantes."
                        )

                print(f"Total de filas procesadas: {total_rows}")
                print(f"Inserciones exitosas: {successful_inserts}")
                return True
        except Exception as e:
            print(f"Error al importar desde CSV: {e}")
            return False


d = Data()
users = d.returnAllElements()
for i in users:
    print(i)
