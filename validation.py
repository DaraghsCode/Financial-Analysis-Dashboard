import csv
from datetime import datetime
#Steps
#1. read in csv file
#   -identify correct columns exist

#2. remove duplicate rows and store in invalid records

#3. validate each rows values 
#   -missing/invalid values
#   -formatting issues, dates, figures etc
#   if:  issue can be fixed,fix it and keep validated row
#   else: remove invalid rows and store in invalid_records

#4. document all invalid records along with their issue

#5. write new file containing all invalid records

#6. write new validated file
#   -this file will be ready for analysis in workflow.py

#7. print a validation report for quick readability
#   -number of valid rows
#   -number of invalid rows

#checking columns exist
def checkColumnsExist(reader):
    required_columns = {
        "date",
        "revenue",
        "cogs",
        "marketing_expense",
        "salaries",
        "operating_expenses",
        "other_expenses"
    }

    actual_columns = set(reader.fieldnames or [])
    missing_columns = required_columns - actual_columns

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {', '.join(sorted(missing_columns))}"
        )
    return None

#helper function used in checkValues
def removeDuplicateDates(reader):
    print("Removing duplicates...")
    print("...")
    seen=set()
    duplicates=[]
    rows=[]
    for row in reader:
        for field in row.keys():
            if field == 'date':
                if row['date'] in seen:
                    duplicates.append(row)
                else:
                    rows.append(row)
                    seen.add(row['date'])
    #read every row
    #add date to seen
    #if date is already in seen, add to duplicates
    print(f"removed {len(duplicates)} duplicates")
    print(f"number of non-duplicate rows: {len(seen)}")
    return rows,duplicates

#helper function used in checkValues
def checkDateFormat(date):
    expectedFormats=[
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%Y/%m/%d"
    ]
    for format in expectedFormats:
        try:
            dtObject=datetime.strptime(date,format)
            formattedDate=dtObject.strftime("%Y-%m-%d")
            return formattedDate
        except ValueError:
            pass
    return "invalid_date_format"

#helper function used in checkValues
def checkNumberFormat(number):
    #read number and remove comma
    number=number.replace(",","")
    try:
        number=float(number)
        return number
    except ValueError:
        pass
    #if data is not a float
    # return invalid_figure
    #else
    # return figure
    return "invalid_figure"

#Validating every rows values
def checkValues(rows):
    rows,duplicates=removeDuplicateDates(rows)
    invalid_rows=[]
    valid_rows=[]

    for row in duplicates:
        row["issues"]="duplicate entry"
        invalid_rows.append(row)

    for row in rows:
        issues=[]
        for field,value in row.items():
            formattedDate=checkDateFormat(row['date'])
            formattedFigure=checkNumberFormat(row[field])
            #1. checking for missing values(note fill in missing values for analysis.py this is purely just to practice)
            if value == '':
                issues.append(f"missing {field} value")
            elif field == 'date':
                if formattedDate == "invalid_date_format":
                    issues.append("invalid_date")
                else:
                    #if format is accepted, standardize date
                    row['date']=formattedDate
            # if invalid date format, add to invalid rows, issue: invalid date format
            #we are expecting all columns after date to consist of number values
            #thus we can use a single function to check for a valid value
            else:
                if formattedFigure == "invalid_figure":
                    issues.append(f"invalid {field} value")
                else:
                    row[field]=formattedFigure

        
        #after checking all values, if any issues were found, append row and issues to invalid rows
        if len(issues)!=0:
            row["issues"]=issues
            invalid_rows.append(row)
        else:
            valid_rows.append(row)
    return invalid_rows, valid_rows

def writeInvalidRows(invalidRows):
    with open("invalid_rows.csv",mode="w",newline="") as file:
        fieldNames=invalidRows[0].keys()

        writer = csv.DictWriter(file, fieldnames=fieldNames)

        writer.writeheader()
        writer.writerows(invalidRows)
        print("invalid_rows.csv has been successfully written!")
    return 

def writeValidRows(validRows):
    with open("validated_rows.csv",mode="w",newline="") as file:
        fieldNames=validRows[0].keys()

        writer = csv.DictWriter(file, fieldnames=fieldNames)

        writer.writeheader()
        writer.writerows(validRows)
        print("validated_rows.csv has been successfully written!")
    return 

def main():
    with open("sample_pnl_statement.csv") as file:
        reader=csv.DictReader(file)

        checkColumnsExist(reader)
        invalid_rows, valid_rows=checkValues(reader)

        print(f"number of invalid rows: {len(invalid_rows)}")

        if len(invalid_rows) != 0:
            writeInvalidRows(invalid_rows)

        if len(valid_rows) !=0:
            writeValidRows(valid_rows)


if __name__ == "__main__":
    main()
        