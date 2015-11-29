select fst.Year, snd.Year, Country.Name, ((snd.Rate - fst.Rate) / (snd.Year - fst.Year)) Growth from 
    LiteracyRate fst inner join LiteracyRate snd on fst.CountryCode = snd.CountryCode and fst.Year < snd.Year
    inner join Country on fst.CountryCode = Country.code
group by Country.Name, fst.Year
having snd.Year = min(snd.Year)
order by Growth desc;
