select City.Name, City.Population, Country.Population from City inner join Country on Country.Code = City.CountryCode
order by (1.0 * City.Population / Country.Population) desc, City.Name desc limit 20;
