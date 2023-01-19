import csv
# from base.models import Setting

with open("C:/Users/PC/Desktop/T_SESSION_DATA.csv") as f:
  data = csv.reader(f)

  for row in data:
        # row = Staff(**datum)
        # row.save()
        print(row)
    