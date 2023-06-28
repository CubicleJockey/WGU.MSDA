SELECT p.children
	  ,p.age
	  ,p.income
	  ,p.marital
	  ,p.readmis AS "Readmission"
	  ,p.gender
	  ,p.initial_days
	  ,p.totalcharge
	  ,p.additional_charges
	  ,p.vitd_levels
	  ,p.doc_visits
	  ,p.full_meals
	  ,p.vitd_supp
	  ,p.soft_drink
	  ,p.hignblood AS "HighBlood"
	  ,p.stroke
	  ,l.zip
	  ,l.city
	  ,l.state
	  ,l.county
	  ,c.complication_risk
	  ,admin.initial_admission
FROM patient AS p
	INNER JOIN location AS l ON l.location_id = p.location_id
	INNER JOIN complication AS c ON c.complication_id = p.compl_id
	INNER JOIN admission AS admin ON admin.admins_id = p.admis_id