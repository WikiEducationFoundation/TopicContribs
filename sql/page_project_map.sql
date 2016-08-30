-- To be run on wmflabs
SET net_read_timeout = 100000;
DROP TABLE IF EXISTS <user_database>.tmp_page_categorylinks;
CREATE TEMPORARY TABLE <user_database>.tmp_page_categorylinks AS
(
    select article.page_id as page_id, cl.cl_to as cl_to
    from enwiki_p.page as article
    join enwiki_p.page as tp
    on tp.page_namespace = 1 AND tp.page_title = article.page_title
    join ( select *
           from enwiki_p.categorylinks as rcl
           where rcl.cl_to LIKE "%importance\_%\_articles%" OR
                 rcl.cl_to LIKE "%Class\_%\_articles%" ) as cl
    on cl.cl_from = tp.page_id
);


SELECT DISTINCT page_id, if(cl_to LIKE "%importance\_%\_articles%",
                            SUBSTRING(cl_to,
                                LOCATE('importance_', cl_to) + 11,
                                LOCATE('_articles', cl_to) - (LOCATE('importance_', cl_to) + 11)),
                            SUBSTRING(cl_to,
                                LOCATE('Class_', cl_to) + 6,
                                LOCATE('_articles', cl_to) - (LOCATE('Class_', cl_to) + 6))
                ) as project
FROM <user_database>.tmp_page_categorylinks;
