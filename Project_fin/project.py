import sqlite3

conn = sqlite3.connect('grant.db')
cursor = conn.cursor()

create_grant_competition_table = """
CREATE TABLE GrantCompetition(
    competitionID INTEGER PRIMARY KEY,
    topic TEXT NOT NULL
)
"""

create_researchers_table = """
CREATE TABLE Researchers(
    researcherID INTEGER PRIMARY KEY,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    email TEXT NOT NULL,
    organization TEXT NOT NULL
)
"""

create_grant_calls_table = """
CREATE TABLE GrantCalls(
    number INTEGER NOT NULL,
    title TEXT NOT NULL,
    applicationDeadline DATE NOT NULL,
    description TEXT NOT NULL,
    area TEXT NOT NULL,
    competitionStatus TEXT NOT NULL,
    PRIMARY KEY (number, applicationDeadline),
    FOREIGN KEY (area) REFERENCES GrantCompetition(topic)
)
"""

create_submitted_grant_application_table = """
CREATE TABLE SubmittedGrantApplication(
    applicationID INTEGER PRIMARY KEY,
    requestedAmount DECIMAL(10, 2) NOT NULL,
    competitionID INTEGER NOT NULL,
    principleInvestigatorID INTEGER NOT NULL,
    applicationStatus TEXT NOT NULL,
    awardAmount DECIMAL(10, 2),
    awardDate DATE,
    FOREIGN KEY (competitionID) REFERENCES GrantCompetition(competitionID),
    FOREIGN KEY (principleInvestigatorID) REFERENCES Researchers(researcherID)
)
"""

create_collaborators_table = """
CREATE TABLE Collaborators(
    applicationID INTEGER,
    collaboratorID INTEGER,
    PRIMARY KEY (applicationID, collaboratorID),
    FOREIGN KEY (applicationID) REFERENCES SubmittedGrantApplication(applicationID),
    FOREIGN KEY (collaboratorID) REFERENCES Researchers(researcherID)
);
"""

create_reviewers_table = """
CREATE TABLE Reviewers(
    reviewerID INTEGER PRIMARY KEY,
    FOREIGN KEY (reviewerID) REFERENCES Researchers(researcherID)
);
"""

create_records_table = """
CREATE TABLE Records(
    applicationID INTEGER PRIMARY KEY,
    reviewerID INTEGER,
    coReviewer1ID INTEGER,
    coReviewer2ID INTEGER,
    FOREIGN KEY (applicationID) REFERENCES SubmittedGrantApplication(applicationID),
    FOREIGN KEY (reviewerID) REFERENCES Reviewers(reviewerID),
    FOREIGN KEY (coReviewer1ID) REFERENCES Reviewers(reviewerID),
    FOREIGN KEY (coReviewer2ID) REFERENCES Reviewers(reviewerID)
);
"""

create_conflict_of_interest_table = """
CREATE TABLE ConflictOfInterest(
    reviewerID INTEGER,
    conflictResearcherID INTEGER,
    conflictDescription TEXT,
    PRIMARY KEY (reviewerID, conflictResearcherID),
    FOREIGN KEY (reviewerID) REFERENCES Reviewers(reviewerID),
    FOREIGN KEY (conflictResearcherID) REFERENCES Researchers(researcherID)
);
"""

create_reviewer_assignment_table = """
CREATE TABLE ReviewerAssignment(
    assignmentID INTEGER PRIMARY KEY,
    competitionID INTEGER NOT NULL,
    reviewerID INTEGER NOT NULL,
    deadline DATE NOT NULL,
    reviewStatus TEXT NOT NULL,
    FOREIGN KEY (competitionID) REFERENCES GrantCompetition(competitionID),
    FOREIGN KEY (reviewerID) REFERENCES Reviewers(reviewerID)
);
"""

create_meeting_table = """
CREATE TABLE Meeting(
    meetingID INTEGER PRIMARY KEY,
    meetingDate DATE NOT NULL
);
"""

create_meeting_attendance_table = """
CREATE TABLE MeetingAttendance(
    meetingID INTEGER,
    reviewerID INTEGER,
    competitionID INTEGER,
    assignmentID INTEGER,
    PRIMARY KEY (meetingID, reviewerID, assignmentID),
    FOREIGN KEY (meetingID) REFERENCES Meeting(meetingID),
    FOREIGN KEY (reviewerID) REFERENCES Reviewers(reviewerID),
    FOREIGN KEY (competitionID) REFERENCES GrantCompetition(competitionID)
    FOREIGN KEY (assignmentID) REFERENCES ReviewerAssignment(assignmentID)
);
"""

cursor.execute(create_grant_competition_table)
cursor.execute(create_researchers_table)
cursor.execute(create_grant_calls_table)
cursor.execute(create_submitted_grant_application_table)
cursor.execute(create_collaborators_table)
cursor.execute(create_reviewers_table)
cursor.execute(create_records_table)
cursor.execute(create_conflict_of_interest_table)
cursor.execute(create_reviewer_assignment_table)
cursor.execute(create_meeting_table)
cursor.execute(create_meeting_attendance_table)

conn.commit()
conn.close()