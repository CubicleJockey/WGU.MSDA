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