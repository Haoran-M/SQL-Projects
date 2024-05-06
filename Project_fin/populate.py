import sqlite3

conn = sqlite3.connect('grant.db')
cursor = conn.cursor()

insert_grant_competition = """
INSERT INTO GrantCompetition (competitionID, topic) 
VALUES  (1101, 'Biomedical Research'),
        (1102, 'Renewable Energy'),
        (1103, 'Artificial Intelligence'),
        (1104, 'Climate Change Mitigation'),
        (1105, 'Data Science'),
        (1106, 'Robotics'),
        (1107, 'Nanotechnology'),
        (1108, 'Cybersecurity'),
        (1109, 'Agricultural Innovation'),
        (1110, 'Space Exploration');
"""

insert_researchers = """
INSERT INTO Researchers (researcherID, firstName, lastName, email, organization) 
VALUES  (201, 'John', 'Doe', 'john.doe@example.com', 'ABC University'),
        (202, 'Jane', 'Smith', 'jane.smith@example.com', 'XYZ Research Institute'),
        (203, 'Michael', 'Johnson', 'michael.johnson@example.com', 'University of Science'),
        (204, 'Emily', 'Brown', 'emily.brown@example.com', 'Institute of Technology'),
        (205, 'David', 'Wilson', 'david.wilson@example.com', 'Center for Research'),
        (206, 'Sarah', 'Lee', 'sarah.lee@example.com', 'National Laboratory'),
        (207, 'Daniel', 'Martinez', 'daniel.martinez@example.com', 'Tech Innovations'),
        (208, 'Jessica', 'Taylor', 'jessica.taylor@example.com', 'Institute of Advanced Studies'),
        (209, 'Andrew', 'Anderson', 'andrew.anderson@example.com', 'Research Foundation'),
        (210, 'Sophia', 'Garcia', 'sophia.garcia@example.com', 'Space Agency'),
        (211, 'Jay', 'Down', 'joy.down4@example.com', 'ABC University'),
        (212, 'Jane', 'Smith', 'jane.smith4@example.com', 'XYZ Research Institute'),
        (213, 'Mich', 'John', 'mich.john@example.com', 'University of Science'),
        (214, 'Emily', 'Brown', 'emily.brown4@example.com', 'Institute of Technology'),
        (215, 'Davy', 'Wilson', 'davy.wilson@example.com', 'Center for Research'),
        (216, 'Sara', 'Lee', 'sara.lee@example.com', 'National Laboratory'),
        (217, 'Daniel', 'Martin', 'daniel.martin@example.com', 'Tech Innovations'),
        (218, 'Jessica', 'Taylor', 'jessica.taylor4@example.com', 'Institute of Advanced Studies'),
        (219, 'Andrea', 'Anderson', 'andrea.anderson4@example.com', 'Research Foundation'),
        (220, 'Andrew', 'Garcia', 'andrew.garcia4@example.com', 'Space Agency');
""" 

insert_grant_calls = """
INSERT INTO GrantCalls (number, title, applicationDeadline, description, area, competitionStatus) 
VALUES  (1201, 'Biomedical Research Grants 2024', '2024-05-15', 'Funding for biomedical research projects', 'Biomedical Research', 'Open'),
        (1202, 'Renewable Energy Projects 2024', '2024-06-30', 'Funding for renewable energy initiatives','Renewable Energy', 'Open'),
        (1203, 'AI Research Fund 2024', '2024-07-15', 'Support for artificial intelligence research','Artificial Intelligence', 'Open'),
        (1204, 'Climate Change Solutions Grant 2024', '2024-08-20', 'Funding for projects addressing climate change', 'Climate Change Mitigation', 'Open'),
        (1205, 'Data Science Innovation Grants 2024', '2024-09-25', 'Support for innovative data science projects', 'Data Science', 'Open'),
        (1206, 'Robotics Development Fund 2024', '2024-10-10', 'Funding for advancements in robotics technology', 'Robotics', 'Open'),
        (1207, 'Nanotechnology Research Grants 2024', '2024-11-05', 'Support for nanotechnology research projects', 'Nanotechnology', 'Open'),
        (1208, 'Cybersecurity Initiative Grants 2024', '2024-12-15', 'Funding for cybersecurity initiatives','Cybersecurity', 'Open'),
        (1209, 'Agricultural Innovation Fund 2024', '2025-01-20', 'Support for innovative agricultural projects','Agricultural Innovation', 'Open'),
        (1210, 'Space Exploration Grants 2024', '2025-02-28', 'Funding for space exploration initiatives','Space Exploration', 'Open');
"""

insert_submitted_grant_application = """
INSERT INTO SubmittedGrantApplication (applicationID, requestedAmount, competitionID, principleInvestigatorID, applicationStatus, awardAmount, awardDate) 
VALUES  (301, 22000.00, 1103, 205, 'Submitted', NULL, 'NULL'),
        (302, 30000.00, 1104, 207, 'Awarded', 35000.00, '2024-04-05'),
        (303, 1800.00, 1105, 210, 'Submitted', NULL, 'NULL'),
        (304, 3500.00, 1103, 220, 'Submitted', NULL, 'NULL'),
        (305, 2500.00, 1107, 204, 'Awarded', 2500.00, '2024-01-13'),
        (306, 4000.80, 1108, 216, 'Not Awarded', NULL, 'NULL'),
        (307, 28000.00, 1109, 219, 'Submitted', NULL, 'NULL'),
        (308, 3000.00, 1110, 211, 'Submitted', NULL, 'NULL'),
        (309, 3200.00, 1105, 214, 'Submitted', NULL, 'NULL'),
        (310, 18000.00, 1103, 217, 'Awarded', 19000.00, '2024-03-18');
"""

insert_collaborators = """
INSERT INTO Collaborators(applicationID, collaboratorID)
VALUES  (301, 205), (301, 206),
        (302, 207), (302, 208), (302, 209),
        (303, 210), (303, 211),
        (304, 220), (304, 202), (304, 203),
        (305, 204), (305, 215),
        (306, 216), (306, 217), (306, 218),
        (307, 219), (307, 210),
        (308, 211), (308, 213),
        (309, 214), (309, 215),
        (310, 217), (310, 205), (310, 216);
"""

insert_reviewers = """
INSERT INTO Reviewers (reviewerID) 
VALUES  (201), 
        (202),
        (203), 
        (204), 
        (205), 
        (206), 
        (207), 
        (208), 
        (209), 
        (210);       
"""
insert_records = """
INSERT INTO Records (applicationID, reviewerID, coReviewer1ID, coReviewer2ID) 
VALUES  (301, 201, NULL, NULL),
        (302, 201, 202, 203),
        (303, 201, 205, NULL),
        (304, 208, NULL, NULL),
        (305, 206, 209, 210),
        (306, 207, 209, 210),
        (307, 202, NULL, NULL),
        (308, 210, NULL, NULL),
        (309, 204, 205, NULL),
        (310, 204, 205, 208);
"""

insert_conflict_of_interest = """
INSERT INTO ConflictOfInterest (reviewerID, conflictResearcherID, conflictDescription) 
VALUES  (201, 211, 'Same institution'), 
        (202, 212, 'Same institution'),
        (202, 203, 'Co-authored a paper in the past two years'),
        (202, 220, 'Co-authored a paper in the past two years'),
        (203, 213, 'Same institution'),
        (203, 202, 'Co-authored a paper in the past two years'),
        (204, 214, 'Same institution'),
        (204, 215, 'Co-authored a paper in the past two years'),
        (205, 215, 'Same institution'),
        (205, 206, 'Co-authored a paper in the past two years'),
        (205, 216, 'Co-authored a paper in the past two years'),
        (205, 217, 'Co-authored a paper in the past two years'),
        (206, 216, 'Same institution'),
        (206, 205, 'Co-authored a paper in the past two years'),
        (207, 217, 'Same institution'),
        (207, 208, 'Co-authored a paper in the past two years'),
        (207, 219, 'Co-authored a paper in the past two years'),
        (208, 218, 'Same institution'),
        (208, 207, 'Co-authored a paper in the past two years'),
        (209, 219, 'Same institution'),
        (210, 220, 'Same institution'),
        (210, 211, 'Co-authored a paper in the past two years'),
        (210, 219, 'Co-authored a paper in the past two years');
"""

insert_reviewer_assignment = """
INSERT INTO ReviewerAssignment (assignmentID, competitionID, reviewerID, deadline, reviewStatus) 
VALUES  (001, 1103, 201, '2024-05-01', 'Submitted'),
        (002, 1104, 201, '2024-03-01', 'Submitted'),
        (003, 1105, 201, '2024-05-01', 'Not Submitted'),
        (004, 1104, 202, '2024-03-01', 'Submitted'),
        (005, 1109, 202, '2024-05-01', 'Not Submitted'),
        (006, 1104, 203, '2024-03-01', 'Submitted'),
        (007, 1105, 204, '2024-05-01', 'Submitted'),
        (008, 1103, 204, '2024-03-01', 'Submitted'),
        (009, 1105, 205, '2024-05-01', 'Submitted'),
        (010, 1105, 205, '2024-05-01', 'Submitted'),
        (011, 1103, 205, '2024-03-01', 'Submitted'),
        (012, 1107, 206, '2024-01-01', 'Submitted'),
        (013, 1108, 207, '2024-03-01', 'Submitted'),
        (014, 1103, 208, '2024-03-01', 'Submitted'),
        (015, 1103, 208, '2024-03-01', 'Submitted'),
        (016, 1107, 209, '2024-01-01', 'Submitted'),
        (017, 1105, 209, '2024-01-01', 'Submitted'),
        (018, 1107, 210, '2024-01-01', 'Submitted'),
        (019, 1108, 210, '2024-03-01', 'Submitted'),
        (020, 1110, 210, '2024-05-01', 'Not Submitted');
"""

insert_meeting = """
INSERT INTO Meeting (meetingID, meetingDate) 
VALUES  (401, '2024-01-05'),
        (402, '2024-03-10'),
        (403, '2024-04-01'),
        (404, '2024-05-10');
"""

insert_meeting_attendance = """
INSERT INTO MeetingAttendance (meetingID, reviewerID, competitionID, assignmentID) 
VALUES  (401, 206, 1107, 305), (401, 209, 1107, 305), (401, 210, 1107, 305),
        (402, 207, 1108, 306), (402, 209, 1108, 306), (402, 210, 1108, 306), (402, 204, 1103, 310), (402, 205, 1103, 310), (402, 208, 1103, 310),
        (403, 201, 1104, 302), (403, 202, 1104, 302), (403, 203, 1104, 302),
        (404, 201, 1103, 301),
        (404, 201, 1105, 303), (404, 205, 1105, 303),
        (404, 208, 1103, 304), 
        (404, 202, 1109, 307), 
        (404, 210, 1110, 308), 
        (404, 204, 1105, 309), (404, 205, 1105, 309);
"""

cursor.execute(insert_grant_competition)
cursor.execute(insert_researchers)
cursor.execute(insert_grant_calls)
cursor.execute(insert_submitted_grant_application)
cursor.execute(insert_collaborators)
cursor.execute(insert_reviewers)
cursor.execute(insert_records)
cursor.execute(insert_conflict_of_interest)
cursor.execute(insert_reviewer_assignment)
cursor.execute(insert_meeting)
cursor.execute(insert_meeting_attendance)

conn.commit()
conn.close()