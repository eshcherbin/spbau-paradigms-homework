select Name, Rate, Year from Country, LiteracyRate
where CountryCode = Country.Code
group by Name having max(Year) = Year
order by Rate desc limit 1;
