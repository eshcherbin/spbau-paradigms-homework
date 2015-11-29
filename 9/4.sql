select Country.Name, count(distinct City.Name) CityCount from 
    Country left join City on City.CountryCode = Country.Code and City.Population >= 1000000
group by Country.Name
order by CityCount desc, Country.name;
