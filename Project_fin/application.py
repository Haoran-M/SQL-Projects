import sqlite3

def print_all_areas():
    conn = sqlite3.connect('grant.db')
    cursor = conn.cursor()

    query = """
    SELECT DISTINCT area
    FROM GrantCalls;
    """

    cursor.execute(query)
    areas = cursor.fetchall()

    conn.close()

    if areas:
        print("All Areas:")
        for area in areas:
            print(area[0])
    else:
        print("No areas found.")



def find_open_competitions(month):
    conn = sqlite3.connect('grant.db')
    cursor = conn.cursor()

    query = """
    SELECT gc.number, gc.title
    FROM GrantCalls gc
    WHERE strftime('%m', gc.applicationDeadline) = :specified_month
    AND EXISTS (
        SELECT 1
        FROM SubmittedGrantApplication sga
        JOIN GrantCompetition gcomp ON sga.competitionID = gcomp.competitionID
        WHERE gc.area = gcomp.topic
        AND (sga.requestedAmount > 20000 OR (
            SELECT COUNT(*)
            FROM Collaborators coll
            WHERE coll.applicationID = sga.applicationID
        ) > 10)
    );
    """

    cursor.execute(query, {'specified_month': month.zfill(2)})
    competitions = cursor.fetchall()

    conn.close()
    return competitions

def find_largest_requested_amount(area):
    conn = sqlite3.connect('grant.db')
    cursor = conn.cursor()

    query = """
    SELECT sga.applicationID, sga.requestedAmount
    FROM SubmittedGrantApplication sga
    JOIN GrantCompetition gc ON sga.competitionID = gc.competitionID
    WHERE gc.topic = ?
    ORDER BY sga.requestedAmount DESC
    LIMIT 1;
    """

    cursor.execute(query, (area,))
    result = cursor.fetchone()

    conn.close()
    return result

def find_largest_awarded_amount_before_date(date):
    conn = sqlite3.connect('grant.db')
    cursor = conn.cursor()

    query = """
    SELECT sga.applicationID, sga.awardAmount
    FROM SubmittedGrantApplication sga
    WHERE sga.awardDate < ?
    ORDER BY sga.awardAmount DESC
    LIMIT 1;
    """

    cursor.execute(query, (date,))
    result = cursor.fetchone()

    conn.close()
    return result

def find_proposals_for_reviewer(reviewer_name):
    conn = sqlite3.connect('grant.db')
    cursor = conn.cursor()

    query = """
    SELECT rec.applicationID
    FROM Records rec
    JOIN Reviewers rev ON rec.reviewerID = rev.reviewerID
    JOIN Researchers res ON rev.reviewerID = res.researcherID
    WHERE res.firstName || ' ' || res.lastName = ? 
       OR rec.coReviewer1ID = rev.reviewerID
       OR rec.coReviewer2ID = rev.reviewerID;
    """

    cursor.execute(query, (reviewer_name,))
    proposals = cursor.fetchall()

    conn.close()
    return proposals if proposals else []


def calculate_requested_awarded_discrepancy(area):
    conn = sqlite3.connect('grant.db')
    cursor = conn.cursor()

    query = """
    SELECT AVG(ABS(requestedAmount - awardAmount))
    FROM SubmittedGrantApplication sga
    JOIN GrantCompetition gc ON sga.competitionID = gc.competitionID
    WHERE gc.topic = ?;
    """

    cursor.execute(query, (area,))
    result = cursor.fetchone()[0]

    conn.close()
    return result


def get_available_reviewers():
    conn = sqlite3.connect('grant.db')
    cursor = conn.cursor()

    # Query to get reviewers who haven't reached the maximum limit
    query = """
    SELECT DISTINCT rev.reviewerID
    FROM Reviewers rev
    WHERE rev.reviewerID NOT IN (
        SELECT DISTINCT reviewerID
        FROM Records
    )
    GROUP BY rev.reviewerID
    HAVING COUNT(*) < 3;
    """

    cursor.execute(query)
    reviewer_ids = cursor.fetchall()

    conn.close()
    return reviewer_ids



def get_null_reviewer_entries():
    conn = sqlite3.connect('grant.db')
    cursor = conn.cursor()

    # Query to get entries where reviewerID is not null but either coReviewer1ID or coReviewer2ID is null
    query = """
    SELECT applicationID, coReviewer1ID, coReviewer2ID
    FROM Records
    WHERE reviewerID IS NOT NULL
    AND (coReviewer1ID IS NULL OR coReviewer2ID IS NULL);
    """

    cursor.execute(query)
    null_entries = cursor.fetchall()

    conn.close()
    return null_entries

def update_record_with_reviewer(application_id, reviewer_id):
    conn = sqlite3.connect('grant.db')
    cursor = conn.cursor()

    # Query to select the row where either coReviewer1ID or coReviewer2ID is NULL
    query = """
    SELECT applicationID, coReviewer1ID, coReviewer2ID
    FROM Records
    WHERE applicationID = ? AND (coReviewer1ID IS NULL OR coReviewer2ID IS NULL);
    """

    cursor.execute(query, (application_id,))
    row = cursor.fetchone()

    if row:
        application_id, co_reviewer1_id, co_reviewer2_id = row
        null_column = None
        if co_reviewer1_id is None:
            null_column = "coReviewer1ID"
        elif co_reviewer2_id is None:
            null_column = "coReviewer2ID"

        if null_column:
            # Update the record with the reviewer ID
            update_query = f"""
            UPDATE Records
            SET {null_column} = ?
            WHERE applicationID = ?;
            """
            cursor.execute(update_query, (reviewer_id, application_id))
            print(f"Reviewer ID {reviewer_id} inserted successfully for application ID {application_id} in column {null_column}.")
        else:
            print("Both coReviewer1ID and coReviewer2ID are already assigned.")
    else:
        print("No rows found with NULL columns for the specified application ID.")

    # Commit changes and close connection
    conn.commit()
    conn.close()



def main():
    while True:
        print("\n Choose an option:")
        print("1. Find open competitions for a specific month.")
        print("2. Find the proposal(s) that request(s) the largest amount of money for a user-specified area.")
        print("3. Find the proposals submitted before a user-specified date that are awarded the largest amount of money.")
        print("4. Output the average requested/awarded discrepancy for a user-specified area.")
        print("5. Find the proposal(s) a specified reviewer needs to review.")
        print("6. Assign reviewers to review a specific grant application.")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            month = input("Enter the month (MM): ")
            competitions = find_open_competitions(month)
            if competitions:
                print("Open Competitions:")
                for competition in competitions:
                    print(f"Competition ID: {competition[0]}, Title: {competition[1]}")
            else:
                print("No open competitions found for the specified month.")
        elif choice == '2':
            print_all_areas()
            area = input("Enter the area: ")
            result = find_largest_requested_amount(area)
            if result:
                print(f"The proposal with the largest requested amount in {area} is:")
                print(f"Proposal ID: {result[0]}, Requested Amount: {result[1]}")
            else:
                print("No proposals found for the specified area.")
        elif choice == '3':
            date = input("Enter the date (YYYY-MM-DD): ")
            result = find_largest_awarded_amount_before_date(date)
            if result:
                print(f"The proposal awarded the largest amount before {date} is:")
                print(f"Proposal ID: {result[0]}, Awarded Amount: {result[1]}")
            else:
                print("No proposals found before the specified date.")
        elif choice == '4':
            area = input("Enter the area: ")
            result = calculate_requested_awarded_discrepancy(area)
            print(f"The average requested/awarded discrepancy in {area} is: {result}")
        elif choice == '5':
            reviewer_name = input("Enter the reviewer's full name (e.g., John Doe): ")
            proposals = find_proposals_for_reviewer(reviewer_name)
            if proposals:
                print(f"The proposal(s) that {reviewer_name} needs to review:")
                for proposal in proposals:
                    print(f"Proposal ID: {proposal[0]}")  # Printing only the proposal ID
            else:
                print(f"No proposals found for {reviewer_name}.")
        elif choice == '6':
            null_entries = get_null_reviewer_entries()

            if not null_entries:
                print("No entries found where reviewer ID is not null and coReviewer1ID or coReviewer2ID is null.")
                return

            for entry in null_entries:
                application_id, co_reviewer1_id, co_reviewer2_id = entry
                print(f"Application ID: {application_id}, coReviewer1ID: {co_reviewer1_id}, coReviewer2ID: {co_reviewer2_id}")
            
            # Print available reviewers
            print("Available Reviewers:")
            available_reviewers = get_available_reviewers()
            for reviewer_ids in available_reviewers:
                print(f"Reviewer ID: {reviewer_ids[0]}")
                
            application_id = input("Enter the application ID: ")
            
            # Ask for the reviewer ID to insert
            reviewer_id = input("Enter the reviewer ID to insert: ")
            
            # Update the record with the reviewer ID
            update_record_with_reviewer(application_id, reviewer_id)
           # print(f"Reviewer ID {reviewer_id} inserted successfully for application ID {application_id} in column {null_entries[0]}.")

        elif choice == '7':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()