/*
 File: hospitaloverallranking-per-state-and-rank.sql
 Student: André Davis
 Student ID: 010630641
 Performance Assesment: SLM1 — TASK 1: DATA ANALYSIS - Advanced Acquisition - D211
 Description:
 	Each state has an Hospital Overall Ranking which is on a scale of 1-5 or "Not Available".
	
	This query groups the Hospital OVer All Rankings into their state buckets. From there with Paritioning
	the Rankings are applied to the Hospital Overall Rankings to Rank the scaling.

	Example:
	
	Alaska Hospital Overall Rating Scores:
	
	Scale:				Rank For State:
	------				---------------
	1					1
	2					5
	3					6
	4					4
	5					2
	"Not Available"		3
	
	In this example a score of 1 took the Rank of 1 meaning that their top score is a Hospital Overall Raking of 1.
	This means they worst score is their most selected rating and that should be looked into.
*/
WITH State_OverallRanking_By_State_And_Rating AS (
	SELECT rating."State" AS State
		  ,rating."HospitalOverallRating" AS HospitalOverallRating
		  ,COUNT(rating."HospitalOverallRating") AS HospitalOverallRatingCount
	FROM public.ratings AS rating
	GROUP BY  rating."State", rating."HospitalOverallRating"
	ORDER BY rating."State"
)

SELECT 
	 sobsar.State
	,sobsar.HospitalOverallRating
	,RANK() OVER (PARTITION BY sobsar.State ORDER BY sobsar.HospitalOverallRatingCount) AS Ranking
FROM State_OverallRanking_By_State_And_Rating AS sobsar
ORDER BY sobsar.State ASC, Ranking DESC