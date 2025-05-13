from database.DB_connect import DBConnect
from model.product import Product

class DAO():

    @staticmethod
    def getAllNodes( colore, anno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []
        query = """select p.Product_number, p.Product_line, p.Product_type, p.Product, p.Product_brand, p.Product_color, p.Unit_cost, p.Unit_price
                    from go_products p, go_daily_sales s
                    where p.Product_number = s.Product_number and p.Product_color = %s and Year(s.Date) = %s
                    """

        cursor.execute(query, (colore,anno))

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
        query = """select distinct p1.Product_number, p2.Product_number, count(*) as weight
                from (select  p.Product_number, s.Date, s.Retailer_code
                from go_products p, go_daily_sales s
                where p.Product_number = s.Product_number and p.Product_color = %s and YEAR(s.Date) = %s ) p1, (select  p.Product_number, s.Date, s.Retailer_code
                from go_products p, go_daily_sales s
                where  p.Product_number = s.Product_number and p.Product_color = %s and YEAR(s.Date) = %s ) p2
                where p1.Date = p2.Date and p1.Retailer_code = p2.Retailer_code and p1.Product_number < p2.Product_number
                group by p1.Retailer_code 
                    """

        cursor.execute(query, (colore, anno, colore, anno))

        for row in cursor:
            result.append((row["Product_number"], row["Product_number"], row["weight"]))
            # result.append(ArtObject(object_id = row["object_id"], ...))


        cursor.close()
        conn.close()
        return result