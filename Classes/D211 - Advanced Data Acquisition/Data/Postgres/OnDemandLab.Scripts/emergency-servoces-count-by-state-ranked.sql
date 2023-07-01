/*
 File: emergency-services-count-by-state-ranked.sql
 Student: André Davis
 Student ID: 010630641
 Performance Assesment: SLM1 — TASK 1: DATA ANALYSIS - Advanced Acquisition - D211
 Description:
 	This script will count the number of emergencies service count per state and rank them.
*/
WITH Emergency_Counts_By_State AS (
	SELECT 
		 rating."State" AS State
		,COUNT(*) AS EmergencyServiceCount
	FROM public.ratings AS rating
	GROUP BY rating."State", rating."EmergencyServices"
	ORDER BY rating."State"
)

SELECT ecbs.State
      ,ecbs.EmergencyServiceCount
	  ,DENSE_RANK() OVER(ORDER BY ecbs.EmergencyServiceCount DESC) AS Rank
FROM Emergency_Counts_By_State AS ecbs
WHERE ecbs.State NOT IN ('GU', 'PR', 'VI', 'MP', 'AS') --Exclude Territories
ORDER BY ecbs.State, Rank