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
	  ,DENSE_RANK() OVER(ORDER BY ecbs.EmergencyServiceCount DESC)
FROM Emergency_Counts_By_State AS ecbs;


