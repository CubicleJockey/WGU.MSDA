/*
 File: patient-count-by-state-with-ranking.sql
 Student: André Davis
 Student ID: 010630641
 Performance Assesment: SLM1 — TASK 1: DATA ANALYSIS - Advanced Acquisition - D211
 Description:
 	This script will count the number of patients per state and rank them.
*/
WITH Patient_Count_By_States AS (
	SELECT l.state
		  ,COUNT(p.*) AS PatientCount
	FROM patient AS p
		INNER JOIN location AS l ON l.location_id = p.location_id
	GROUP BY l.State
	ORDER BY l.State
)

SELECT
	pcbs.state
   ,pcbs.PatientCount
   ,DENSE_RANK() OVER (ORDER BY pcbs.PatientCount DESC) AS Ranking
FROM Patient_Count_By_States AS pcbs
ORDER BY state ASC, Ranking DESC;