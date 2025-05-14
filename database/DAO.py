from database.DB_connect import DBConnect
from model.product import Product

class DAO():

    @staticmethod
    def getAllNodes( colore):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []
        query = """select distinct p.Product_number, p.Product_line, p.Product_type, p.Product, p.Product_brand, p.Product_color, p.Unit_cost, p.Unit_price
                    from go_products p, go_daily_sales s
                    where p.Product_number = s.Product_number and p.Product_color = %s 
                    """

        cursor.execute(query, (colore,))

        for row in cursor:
            result.append(Product(**row))
            # result.append(ArtObject(object_id = row["object_id"], ...))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllColor():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []
        query = """select distinct p.Product_color
                    from go_products p, go_daily_sales s
                    where p.Product_number = s.Product_number 
                """

        cursor.execute(query)

        for row in cursor:
            result.append(row["Product_color"])
            # result.append(ArtObject(object_id = row["object_id"], ...))

        cursor.close()
        conn.close()
        return result

    @staticmethod

    def getAllEdges(anno, colore):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []
        query = """SELECT f1.Product_number AS Product1, f2.Product_number AS Product2, COUNT(DISTINCT f1.Date) AS weight
        FROM (
        SELECT gs.Retailer_code, gp.Product_number, gs.Date
        FROM go_products gp
        JOIN go_daily_sales gs ON gp.Product_number = gs.Product_number
        WHERE gp.Product_color = %s AND YEAR(gs.Date) = %s
        ) AS f1
        JOIN (
        SELECT gs.Retailer_code, gp.Product_number, gs.Date
        FROM go_products gp
        JOIN go_daily_sales gs ON gp.Product_number = gs.Product_number
        WHERE gp.Product_color = %s AND YEAR(gs.Date) = %s
        ) AS f2
        ON f1.Retailer_code = f2.Retailer_code
        AND f1.Date = f2.Date
        AND f1.Product_number != f2.Product_number
        GROUP BY f1.Product_number, f2.Product_number
        HAVING COUNT(DISTINCT f1.Date) > 1"""

        cursor.execute(query, (colore, anno, colore, anno))

        for row in cursor:
            result.append((row["Product1"], row["Product2"], row["weight"]))
            # result.append(ArtObject(object_id = row["object_id"], ...))


        cursor.close()
        conn.close()
        return result