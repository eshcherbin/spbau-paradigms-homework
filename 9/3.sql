select City.Name from Country, City, Capital
where Country.Name = "Malaysia" and Capital.CountryCode = Country.Code and Capital.CityId = City.Id;
