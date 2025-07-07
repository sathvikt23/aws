import boto3
import random
from decimal import Decimal
from boto3.dynamodb.conditions import Attr

# Connect to existing table
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('RollNo_EmployeeDB')

# 1. Insert 10 random employees
def insert_employees():
    names = ['Sathvik', 'Neil ', 'Deepa', 'Shanker', 'Sandeep', 'Chandrahaas', 'Shritij', 'Satyam', 'Sudheer', 'Tapadia']
    depts = ['HR', 'IT', 'Finance', 'Sales']
    for i in range(10):
        table.put_item(Item={
            'Employee_No': f'E{i+1}',
            'Employee_Name': names[i],
            'Employee_Dept': random.choice(depts),
            'Employee_sal': Decimal(str(random.randint(10000, 50000)))
        })
    print("Inserted 10 employees.")

# 2. Print employees sorted by Employee_Name
def print_sorted_employees():
    items = table.scan()['Items']
    sorted_items = sorted(items, key=lambda x: x['Employee_Name'])
    print("\n Employees sorted by name:")
    for emp in sorted_items:
        print(f"{emp['Employee_Name']} - {emp['Employee_No']} - {emp['Employee_Dept']} - ₹{emp['Employee_sal']}")

# 3. Total salary of all employees
def total_salary():
    items = table.scan()['Items']
    total = sum(emp['Employee_sal'] for emp in items)
    print(f"\n Total Salary of Employees: ₹{total}")

# 4. Update salary from 10000 to 10500
def update_salary_10000():
    items = table.scan(FilterExpression=Attr('Employee_sal').eq(Decimal('10000')))
    for emp in items['Items']:
        table.update_item(
            Key={'Employee_No': emp['Employee_No']},
            UpdateExpression='SET Employee_sal = :new',
            ExpressionAttributeValues={':new': Decimal('10500')}
        )
        print(f"Updated {emp['Employee_Name']}'s salary to ₹10500")

# 5. Delete an employee (simulate resignation)
def delete_employee(emp_no):
    table.delete_item(Key={'Employee_No': emp_no})
    print(f"Deleted Employee with Employee_No: {emp_no}")

# === MAIN EXECUTION ===
insert_employees()
print_sorted_employees()
total_salary()
update_salary_10000()
delete_employee('E5') 