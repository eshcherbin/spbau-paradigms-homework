select Country.Name from Country left join City on Country.Code = City.CountryCode
where Country.Population > 0
group by Country.Name
having (Country.Population - sum(City.Population) > sum(City.Population))
order by Country.Name;
