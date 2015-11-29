select Country.Name, Country.Population, Country.SurfaceArea from Country
    left join (City inner join Capital on City.Id = Capital.CityId) capital on Country.Code = city.CountryCode
    inner join City justcity on Country.Code = JustCity.CountryCode
group by Country.Name
having capital.Population != max(justcity.Population)
order by (1.0 * Country.Population / Country.SurfaceArea) desc, Country.Name;
