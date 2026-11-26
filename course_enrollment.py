import datetime
from datetime import datetime
import mysql.connector

class Course_enrollment:
    def __init__(self):
        try:
            self.con=mysql.connector.connect(host="localhost",
                                user="root",password="root",database="course_enrollment")

        except:
            print("Database connection failed")
            self.con=None

    def Enroll(self,student_name,course_name,duration_months,enrollment_date,fee,status):
        if self.con is None:
            return

        if fee<0:
            print("Fee should not be a negative value")
        elif duration_months<=0:
            print("Duration must be a positive value")
        else:
            try:
                cursor=self.con.cursor()
                query="INSERT INTO enrollments(student_name,course_name,duration_months,enrollment_date,fee,status)values(%s,%s,%s,%s,%s,%s)"
                data=(student_name,course_name,duration_months,enrollment_date,fee,status,)
                cursor.execute(query,data)
                self.con.commit()
            except Exception:
                print("Insertion failed")
            finally:
                cursor.close()
    def View(self):
        try:

            print("1.view all")
            print("2.Filter by status")

            ch=int(input("Choose one:"))
            if ch==1:
                print("1.sort by enrollment_date")
                print("2.sort by fee")
                n=int(input("Enter choice:"))
                if n==1:
                 query="SELECT * FROM enrollments ORDER BY enrollment_date DESC"
                elif n==2:
                 query = "SELECT * FROM enrollments ORDER BY fee DESC"
                else:
                    print("invalid choice")
                    return
                cursor=self.con.cursor()
                cursor.execute(query)
                records = cursor.fetchall()
                if records:
                    for row in records:
                        print(row)
                else:
                    print("no values present")
            elif ch==2:
                status = input("Enter status (Active/Completed/Cancelled): ").capitalize()
                query = "SELECT * FROM enrollments WHERE status = %s"
                cursor = self.con.cursor()
                cursor.execute(query,(status,))
                records = cursor.fetchall()
                if records:
                    for row in records:
                        print(row)
                else:
                    print("no values present")
        except Exception:
            print("Error while reading")
        finally:
            cursor.close()




    def Search(self):
     if self.con is None:
           return
     try:
                cursor=self.con.cursor()
                print("\n1. Search by enrollment ID")
                print("2. Search by student name")
                print("3. Search by course name")

                choice = input("Enter choice: ")

                if choice == "1":
                    eid = int(input("Enter enrollment ID: "))
                    query="SELECT * FROM enrollments WHERE enrollment_id = %s"
                    cursor.execute(query, (eid,))


                elif choice == "2":
                    name = input("Enter student name: ")
                    query="SELECT * FROM enrollments WHERE student_name LIKE %s%"
                    cursor.execute(query,("%" + name + "%",))


                elif choice == "3":
                    course = input("Enter course name: ")
                    query="SELECT * FROM enrollments WHERE course_name LIKE %s%"
                    cursor.execute(query, ("%" + course + "%",)
                    )

                else:
                    print("Invalid choice.")
                    return

                records = cursor.fetchall()
                if records:
                    for row in records:
                        print(row)
                else:
                    print("No matching enrollment found.")

     except Exception:
                print("Enrollment ID must be a number.")

     finally:
                cursor.close()

    def Update(self,eid):
            if self.con is None:
               return
            try:
                cursor=self.con.cursor()
                cursor.execute(
                    "SELECT * FROM enrollments WHERE enrollment_id = %s",
                    (eid,))
                record = cursor.fetchone()
                if not record:
                    print("Enrollment not found.")
                    return
                new_status = input(
                    "Enter new status (Active/Completed/Cancelled): ").capitalize()

                if new_status not in ["Active", "Completed", "Cancelled"]:
                    print("Invalid status.")
                    return

                update_fee = input("Do you want to update fee? (yes/no): ").lower()

                if update_fee == "yes":
                    new_fee = int(input("Enter new fee: "))

                    if new_fee < 0:
                        print("Fee must be non-negative.")
                        return

                    query = "UPDATE enrollments SET status = %s, fee = %s WHERE enrollment_id = %s"
                    cursor.execute(query, (new_status, new_fee, eid))

                else:
                    query = " UPDATE enrollments SET status = %s WHERE enrollment_id = %s"
                    cursor.execute(query, (new_status, eid))
                self.con.commit()
                print("Enrollment updated successfully!")

            except Exception:
                print("Cannot perform updation")

            finally:
                cursor.close()

    def Delete(self):
     if self.con is None:
            return
     try:
        ch=int(input("Enter enrollment_id to be deleted:"))
        cursor=self.con.cursor()
        query="DELETE FROM enrollments WHERE enrollment_id=%s"

        n=int(input("Are you sure to delete this record(1.yes 2.No) :"))
        if n==1:
            cursor.execute(query, (ch,))
            self.con.commit()
        else:
              return
     except Exception:
             print("Deletion Failed")

     finally:
          cursor.close()

    def Summary(self):
        if self.con is None:
            return
        try:
            cursor=self.con.cursor()
            query="SELECT COUNT(*),SUM(fee),AVG(fee) from enrollments"
            cursor.execute(query)
            record=cursor.fetchone()
            print("Total Enrollments:",record[0])
            print("Total Fee:",record[1])
            print("Average Fee:",record[2])
            print("Enrollments under each status:")
            query="SELECT status,COUNT(*) from enrollments GROUP BY status"
            cursor.execute(query)
            records=cursor.fetchall()
            if records:
                for row in records:
                    print(row[0],":",row[1])
            else:
                print("no record found")
        except Exception:
            print("Error while creating summary")
        finally:
            cursor.close()



c=Course_enrollment()
while(1):

    print("MENU:")
    print("1.Enroll Student")
    print("2. View All Enrollments")
    print("3.Search Enrollment")
    print("4.Update Enrollment Status")
    print("5.Delete Enrollment")
    print("6.Enrollment Summary")
    print("7.Exit")
    ch=int(input("Enter Choice:"))
    if ch==1:
        student_name=input("Enter Name:")
        course_name=input("Enter course:")
        duration_months=int(input("Enter Number of Months:"))
        enrollment_date = datetime.strptime(input("Enter date: "), "%Y-%m-%d").date()
        fee=int(input("Enter fee:"))
        status=input("Enter status:")
        c.Enroll(student_name,course_name,duration_months,enrollment_date,fee,status)
    elif ch==2:
        c.View()
    elif ch==3:
        c.Search()
    elif ch==4:
        eid = int(input("Enter enrollment ID: "))
        c.Update(eid)
    elif ch==5:
        c.Delete()
    elif ch==6:
        c.Summary()
    elif ch==7:
        exit()
