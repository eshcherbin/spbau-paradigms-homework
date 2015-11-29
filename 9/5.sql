select GovernmentForm, sum(SurfaceArea) SumArea from Country
group by GovernmentForm
order by SumArea desc limit 1;
