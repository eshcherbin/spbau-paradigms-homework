head' :: [a] -> a
head' (x:xs) = x

tail' :: [a] -> [a]
tail' (x:xs) = xs

take' :: Int -> [a] -> [a]
take' n [] = []
take' 0 xs = []
take' n (x:xs) = x:(take' (n - 1) xs)

drop' :: Int -> [a] -> [a]
drop' _ [] = []
drop' 0 xs = xs
drop' n (x:xs) = drop' (n - 1) xs

filter' :: (a -> Bool) -> [a] -> [a]
filter' f xs = [x | x <- xs, f x]

foldl' :: (a -> b -> a) -> a -> [b] -> a
foldl' _ z [] = z
foldl' f z (x:l) = foldl' f (f z x) l

concat' :: [a] -> [a] -> [a]
concat' xs [] = xs
concat' [] xs = xs
concat' (x:xs) ys = x:(concat' xs ys)

quickSort' :: Ord a => [a] -> [a]
quickSort' [] = []
quickSort' (x:xs) = concat' (concat' (quickSort' (filter' ((<) x) xs)) (filter' ((==) x) xs)) (quickSort' (filter' ((>) x) xs))
