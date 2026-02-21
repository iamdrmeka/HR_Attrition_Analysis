USE hr_attriution;
-- sEEING ALL DATA
-- sEEING ALL DATA
-- sEEING ALL DATA
SELECT *
FROM hr_table;
-- check the number of rows in the dataset
-- check the number of rows in the dataset
-- check the number of rows in the dataset
SELECT COUNT(*) AS STAFF_COUNT
FROM hr_table;
-- CHECKING TOTAL ATTRITION RATE
-- CHECKING TOTAL ATTRITION RATE
-- CHECKING TOTAL ATTRITION RATE
SELECT Total_staff,
    total_attrition,
    ROUND((100 * total_attrition) / total_staff, 2) AS attriton_rate
FROM (
        SELECT COUNT(*) AS TOTAL_STAFF,
            SUM(
                CASE
                    WHEN attrition = 'yes' THEN 1
                    ELSE 0
                END
            ) AS total_attrition
        FROM hr_table
    ) T;
-- DEPARTMENT ANALYSIS
-- DEPARTMENT ANALYSIS
-- DEPARTMENT ANALYSIS
WITH department_stat AS (
    SELECT department,
        count(*) AS staff_count_dept,
        SUM(
            CASE
                WHEN attrition = 'yes' THEN 1
                ELSE 0
            END
        ) AS attrited
    FROM hr_table
    GROUP BY department
)
SELECT department,
    staff_count_dept,
    attrited,
    ROUND((100 * attrited) / staff_count_dept, 2) as Attrition_rate,
    (
        SELECT COUNT(DISTINCT(department))
        from hr_table
    ) AS Num_of_dept
FROM department_stat
ORDER BY attrition_rate DESC;
-- checking job satisfaction vs attrition by departments
-- checking job satisfaction vs attrition by departments
-- checking job satisfaction vs attrition by departments
WITH satisfaction_score AS (
    SELECT department,
        COUNT(*) STAFF,
        sum(
            CASE
                WHEN jobsatisfaction = 1 then 1
                else 0
            end
        ) AS SCORE_1,
        sum(
            CASE
                WHEN jobsatisfaction = 2 then 1
                else 0
            end
        ) score_2,
        sum(
            CASE
                WHEN jobsatisfaction = 3 then 1
                else 0
            end
        ) score_3,
        sum(
            CASE
                WHEN jobsatisfaction = 4 then 1
                else 0
            end
        ) score_4
    from hr_table
    WHERE Attrition = 'Yes'
    GROUP BY department
)
SELECT department,
    ROUND((100 * score_1) / staff, 2) SCORE_1,
    ROUND((100 * score_2) / staff, 2) SCORE_2,
    ROUND((100 * score_3) / staff, 2) SCORE_3,
    ROUND((100 * score_4) / staff, 2) SCORE_4
from satisfaction_score;
-- gender analysis
-- gender analysis*/
-- gender analysis
-- create a CTE
WITH gender_stat AS (
    SELECT gender,
        count(*) as staff_count,
        SUM(
            CASE
                WHEN attrition = 'yes' THEN 1
                ELSE 0
            END
        ) AS attrited
    FROM hr_table
    GROUP BY Gender
) -- QUERY GENDER ATTRITION DATA
SELECT gender,
    staff_count,
    attrited,
    ROUND((100 * attrited) / staff_count, 2) AS attrition_rate
FROM gender_stat;
-- Age analysis
-- Age analysis
-- Age analysis
SELECT AGE_RANGE,
    NUMBER_OF_STAFF,
    ATTRITED_STAFF,
    ROUND((100 * ATTRITED_STAFF) / NUMBER_OF_STAFF, 2) AS ATTRITION_RATE
FROM (
        SELECT CASE
                WHEN AGE BETWEEN 18 AND 26 THEN '18-26'
                WHEN AGE BETWEEN 27 AND 35 THEN '27-35'
                WHEN AGE BETWEEN 36 AND 44 THEN '36-44'
                WHEN AGE BETWEEN 45 AND 52 THEN '45-52'
                ELSE '53-60'
            END AS AGE_RANGE,
            count(*) AS NUMBER_OF_STAFF,
            SUM(
                CASE
                    WHEN ATTRITION = 'YES' THEN 1
                    ELSE 0
                END
            ) AS ATTRITED_STAFF
        FROM hr_table
        group by age_range
        ORDER BY AGE_RANGE
    ) T;
-- Age groups and job satisfaction vs attrition.
SELECT age_range,
    SUM(
        CASE
            WHEN JobSatisfaction = 1 THEN 1
            ELSE 0
        END
    ) AS POOR,
    SUM(
        CASE
            WHEN JobSatisfaction = 2 THEN 1
            ELSE 0
        END
    ) AS FAIR,
    SUM(
        CASE
            WHEN JobSatisfaction = 3 THEN 1
            ELSE 0
        END
    ) AS GOOD,
    SUM(
        CASE
            WHEN JobSatisfaction = 4 THEN 1
            ELSE 0
        END
    ) AS GREAT
FROM (
        SELECT CASE
                WHEN AGE BETWEEN 18 AND 26 THEN '18-26'
                WHEN AGE BETWEEN 27 AND 35 THEN '27-35'
                WHEN AGE BETWEEN 36 AND 44 THEN '36-44'
                WHEN AGE BETWEEN 45 AND 52 THEN '45-52'
                ELSE '53-60'
            END AS AGE_RANGE,
            JobSatisfaction
        FROM hr_table
        WHERE attrition = 'yes'
    ) Y
GROUP BY age_range
ORDER BY age_range ASC;
-- overall job satisfaction and attrition number survery
SELECT SUM(
        CASE
            WHEN JobSatisfaction = 1 THEN 1
            ELSE 0
        END
    ) AS POOR,
    SUM(
        CASE
            WHEN JobSatisfaction = 2 THEN 1
            ELSE 0
        END
    ) AS FAIR,
    SUM(
        CASE
            WHEN JobSatisfaction = 3 THEN 1
            ELSE 0
        END
    ) AS GOOD,
    SUM(
        CASE
            WHEN JobSatisfaction = 4 THEN 1
            ELSE 0
        END
    ) AS GREAT
from hr_table
WHERE Attrition = 'yes';
-- cHECKING RELATIONSHIP BETWEEN MARITAL  STATUS AND ATTRITION
SELECT MaritalStatus,
    COUNT(*),
    SUM(
        CASE
            WHEN attrition = 'yes' THEN 1
            ELSE 0
        END
    ) AS attrited_number
from hr_table
GROUP BY maritalstatus;
-- educational field
SELECT Educationfield,
    count(*) STAFF,
    SUM(
        CASE
            WHEN attrition = 'yes' THEN 1
            ELSE 0
        END
    ) AS attrited_number,
    ROUND(
        (
            100 * SUM(
                CASE
                    WHEN attrition = 'yes' THEN 1
                    ELSE 0
                END
            )
        ) / count(*),
        2
    ) Attrition_rate
from hr_table
GROUP BY educationfield;
-- Job Role analysis
SELECT Jobrole,
    count(*),
    SUM(
        CASE
            WHEN attrition = 'yes' THEN 1
            ELSE 0
        END
    ) AS attrited_number,
    ROUND(
        (
            100 * SUM(
                CASE
                    WHEN attrition = 'yes' THEN 1
                    ELSE 0
                END
            ) / count(*)
        ),
        2
    ) as attrition_rate
FROM hr_table
GROUP BY jobrole
ORDER BY attrition_rate DESC;
-- job level analysis
SELECT Joblevel,
    staff_strength,
    attrited,
    ROUND(100 * Attrited / staff_strength, 2) as atrrition_rate
FROM(
        SELECT JOBLEVEL,
            count(*) as staff_strength,
            SUM(
                CASE
                    WHEN attrition = 'yes' THEN 1
                    ELSE 0
                END
            ) AS attrited
        FROM hr_table
        GROUP By joblevel
        order by joblevel
    ) T;
-- Job Involvement analysis
SELECT Jobinvolvement,
    staff_count,
    attrited,
    ROUND(100 * Attrited / staff_count, 2) as atrrition_rate
FROM(
        SELECT Jobinvolvement,
            count(*) as staff_count,
            SUM(
                CASE
                    WHEN attrition = 'yes' THEN 1
                    ELSE 0
                END
            ) AS attrited
        FROM hr_table
        GROUP By JobInvolvementSka
        order by JobInvolvement
    ) T;
-- SALARY RANGE VS ATTRITION RATE
WITH income_stat AS (
    SELECT CASE
            WHEN monthlyincome BETWEEN 1 AND 4800 THEN '1 - 4800'
            WHEN monthlyincome BETWEEN 4800 AND 8600 THEN '4800 - 8600'
            WHEN monthlyincome BETWEEN 8601 AND 12500 THEN '8601 - 12500'
            WHEN monthlyincome BETWEEN 12501 AND 16200 THEN '12501 - 16200'
            WHEN monthlyincome BETWEEN 16200 AND 20000 THEN '16200 - 20000'
            ELSE 'OTHERS'
        END as salary_range,
        CASE
            WHEN monthlyincome BETWEEN 1 AND 4800 THEN 1
            WHEN monthlyincome BETWEEN 4800 AND 8600 THEN 2
            WHEN monthlyincome BETWEEN 8601 AND 12500 THEN 3
            WHEN monthlyincome BETWEEN 12501 AND 16200 THEN 4
            WHEN monthlyincome BETWEEN 16200 AND 20000 THEN 5
            ELSE 'OTHERS'
        END as sort_key,
        count(*) as count,
        SUM(
            CASE
                WHEN attrition = 'yes' THEN 1
                ELSE 0
            END
        ) AS attrited
    FROM hr_table
    GROUP BY salary_range,
        sort_key
)
SELECT salary_range,
    count,
    Attrited,
    ROUND((100 * attrited / count), 2) AS attrition_rate
FROM income_stat
ORDER BY sort_key ASC;
-- OVERTIME VS ATTRITON
SELECT overtime,
    count_staff,
    attrited,
    ROUND((100 * attrited / count_staff), 2) AS Attrition_rate
FROM (
        SELECT overtime,
            count(*) Count_staff,
            SUM(
                CASE
                    WHEN attrition = 'yes' THEN 1
                    ELSE 0
                END
            ) AS attrited
        FROM hr_table
        GROUP BY overtime
    ) T;
-- checking distance from Home
SELECT distancefromhome,
    count(*),
    SUM(
        CASE
            WHEN attrition = 'yes' THEN 1
            ELSE 0
        END
    ) AS attrited
from hr_table
GROUP BY distancefromhome
order by DistanceFromHome;
-- Travel vs attrition
WITH travel_stat AS (
    SELECT BusinessTravel,
        count(*) staff_count,
        SUM(
            CASE
                WHEN attrition = 'yes' THEN 1
                ELSE 0
            END
        ) AS attrited
    from hr_table
    GROUP BY BusinessTravel
    order by BusinessTravel
)
SELECT BusinessTravel,
    staff_count,
    attrited,
    ROUND((100 * attrited / staff_count), 2) AS attrition_rate
FROM travel_stat;
-- promotion Tenure vs attrition
SELECT Tenure,
    staff_count,
    attrited,
    ROUND((100 * attrited / staff_count), 2) AS attrition_rate
from (
        SELECT yearssincelastpromotion as TENURE,
            count(*) STAFF_count,
            SUM(
                CASE
                    WHEN attrition = 'yes' THEN 1
                    ELSE 0
                END
            ) AS attrited
        FROM hr_table
        GROUP BY yearsSinceLastPromotion
    ) t;
-- Number of years worked in company vs attrition
-- grouped into four places.
SELECT TENURE,
    staff_no,
    attrited,
    ROUND((100 * attrited / staff_no), 2) AS attrition_rate
FROM(
        SELECT CASE
                WHEN YearsAtCompany BETWEEN 0 AND 2 THEN "ONBOARDING: 0-2"
                WHEN YearsAtCompany BETWEEN 3 AND 7 THEN 'ESTABLISHED: 3-7'
                WHEN YearsAtCompany BETWEEN 8 AND 15 THEN 'MIDLEVEL: 8-15'
                ELSE 'LONG_TERM: 16+'
            END AS TENURE,
            CASE
                WHEN YearsAtCompany BETWEEN 0 AND 2 THEN 1
                WHEN YearsAtCompany BETWEEN 3 AND 7 THEN 2
                WHEN YearsAtCompany BETWEEN 8 AND 15 THEN 3
                ELSE 4
            END AS sort_key,
            COUNT(*) AS staff_no,
            SUM(
                CASE
                    WHEN attrition = 'yes' THEN 1
                    ELSE 0
                END
            ) AS attrited
        FROM hr_table
        GROUP BY TENURE,
            sort_key
        ORDER BY sort_key
    ) t;
-- YEARS IN CURRENT ROLE
SELECT YearsInCurrentRole,
    COUNT(*) AS number_of_staff,
    SUM(
        CASE
            WHEN Attrition = 'yes' THEN 1
            ELSE 0
        END
    ) AS attrited
FROM hr_table
GROUP BY YearsInCurrentRole
ORDER BY YearsInCurrentRole ASC;
-- YEARS WITH CURERENT MANAGER
SELECT role_tenure,
    number_of_staff,
    attrited,
    ROUND((100 * attrited / number_of_staff), 2) AS atrrition_rate
from (
        SELECT YearsInCurrentRole AS role_tenure,
            COUNT(*) AS number_of_staff,
            SUM(
                CASE
                    WHEN Attrition = 'yes' THEN 1
                    ELSE 0
                END
            ) AS attrited
        FROM hr_table
        GROUP BY YearsInCurrentRole
        ORDER BY YearsInCurrentRole ASC
    ) t;
-- comparing Salary and worklife balance
WITH salary_band AS (
    SELECT *,
        CASE
            WHEN monthlyincome < 3000 THEN 'Low'
            WHEN monthlyincome BETWEEN 3000 AND 7000 THEN 'Medium'
            ELSE 'High'
        END AS salary_group
    FROM hr_table
)
SELECT salary_group,
    worklifebalance,
    COUNT(*) AS total,
    SUM(
        CASE
            WHEN attrition = 'yes' THEN 1
            ELSE 0
        END
    ) AS attrited,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN attrition = 'yes' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS attrition_rate
FROM salary_band
GROUP BY salary_group,
    worklifebalance
ORDER BY attrition_rate DESC;
-- overtime and Job satisfaction vs attrition
SELECT overtime,
    jobsatisfaction,
    COUNT(*) AS total,
    SUM(
        CASE
            WHEN attrition = 'yes' THEN 1
            ELSE 0
        END
    ) AS attrited,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN attrition = 'yes' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS attrition_rate
FROM hr_table
GROUP BY overtime,
    jobsatisfaction
ORDER BY attrition_rate DESC;
SELECT JobSatisfaction
from hr_table
GROUP BY JobSatisfaction;