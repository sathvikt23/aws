import boto3
import random
from decimal import Decimal
from boto3.dynamodb.conditions import Attr

# Connect to existing table
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('RollNo_StudentDB')

# B. Insert 15 random students
def insert_students():
    names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve']
    subjects = ['Math', 'Science', 'English']
    for i in range(15):
        table.put_item(Item={
            'StudentRollNo': f'R{i+1}',
            'StudentName': random.choice(names),
            'FavouriteSubject': random.choice(subjects),
            'SubjectRating': Decimal(str(random.randint(1, 5)))
        })
    print("Inserted 15 students.")

# C. Print students sorted by name
def print_sorted_names():
    items = table.scan()['Items']
    sorted_items = sorted(items, key=lambda x: x['StudentName'])
    print(" Students (Alphabetical Order):")
    for i in sorted_items:
        print(f"{i['StudentName']} - {i['StudentRollNo']}")

# D. Count students with rating 5
def count_rating_5():
    result = table.scan(FilterExpression=Attr('SubjectRating').eq(Decimal('5')))
    print(f" Students with rating 5: {len(result['Items'])}")

# E. Average rating for each subject
def avg_rating():
    items = table.scan()['Items']
    subjects = {}
    for i in items:
        subject = i['FavouriteSubject']
        rating = i['SubjectRating']
        if subject not in subjects:
            subjects[subject] = []
        subjects[subject].append(rating)
    print(" Average Ratings:")
    for s, ratings in subjects.items():
        avg = sum(ratings) / len(ratings)
        print(f"{s}: {round(avg, 2)}")

# F. Update student name by RollNo
def update_name(roll_no, new_name):
    table.update_item(
        Key={'StudentRollNo': roll_no},
        UpdateExpression="SET StudentName = :n",
        ExpressionAttributeValues={':n': new_name}
    )
    print(f" Updated {roll_no}'s name to {new_name}")

# G. Delete duplicate student names
def delete_duplicates():
    items = table.scan()['Items']
    seen = {}
    for i in items:
        name = i['StudentName']
        roll = i['StudentRollNo']
        if name in seen:
            table.delete_item(Key={'StudentRollNo': roll})
            print(f"Deleted duplicate: {roll} ({name})")
        else:
            seen[name] = roll

# Run all steps
insert_students()
print_sorted_names()
count_rating_5()
avg_rating()
update_name('R1', 'UpdatedName')
delete_duplicates()
