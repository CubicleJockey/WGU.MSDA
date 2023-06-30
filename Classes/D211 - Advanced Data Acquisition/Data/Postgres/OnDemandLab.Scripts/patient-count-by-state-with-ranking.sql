/*
 File: 
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

/*
SELECT
	pcbs.state
   ,DENSE_RANK() OVER (PARTITION BY pcbs.PatientCount ORDER BY pcbs.PatientCount DESC) AS Ranking
FROM Patient_Count_By_States AS pcbs
ORDER BY state ASC, Ranking ASC; 
*/