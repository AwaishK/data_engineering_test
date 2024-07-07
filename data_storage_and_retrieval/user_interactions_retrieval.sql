select date(timestamp) as date, count(interaction_id)
from user_interactions_raw
group by date;

select user_id, count(interaction_id) as interactions
from user_interactions_raw
group by user_id
order by interactions desc
FETCH FIRST 2 ROWS ONLY;

select product_id, count(interaction_id) as interactions
from user_interactions_raw
group by product_id
order by interactions desc;
