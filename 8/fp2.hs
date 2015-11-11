import Prelude hiding (lookup)

data BST k v = Empty | Tree k v (BST k v) (BST k v)

lookup :: Ord k => k -> BST k v -> Maybe v
lookup _ Empty = Nothing
lookup k (Tree tk tv left right) | k < tk    = lookup k left
                                 | k > tk    = lookup k right
                                 | otherwise = Just tv

insert :: Ord k => k -> v -> BST k v -> BST k v
insert k v Empty = Tree k v Empty Empty
insert k v (Tree tk tv left right) | k < tk    = Tree tk tv (insert k v left) right
                                   | k > tk    = Tree tk tv left (insert k v right)
                                   | otherwise = Tree k v left right

extract_min :: BST k v -> (Maybe k, Maybe v, BST k v)
extract_min Empty = (Nothing, Nothing, Empty)
extract_min (Tree k v Empty Empty) = (Just k, Just v, Empty)
extract_min (Tree k v Empty right) = (Just k, Just v, Tree rk rv Empty rem_right)
                                     where (Just rk, Just rv, rem_right) = extract_min right
extract_min (Tree k v left right) = (mk, mv, Tree k v rem_left right)
                                    where (mk, mv, rem_left) = extract_min left

extract_max :: BST k v -> (Maybe k, Maybe v, BST k v)
extract_max Empty = (Nothing, Nothing, Empty)
extract_max (Tree k v Empty Empty) = (Just k, Just v, Empty)
extract_max (Tree k v left Empty) = (Just k, Just v, Tree lk lv rem_left Empty)
                                     where (Just lk, Just lv, rem_left) = extract_max left
extract_max (Tree k v left right) = (mk, mv, Tree k v left rem_right)
                                    where (mk, mv, rem_right) = extract_max right

delete :: Ord k => k -> BST k v -> BST k v
delete _ Empty = Empty
delete k (Tree tk tv left right) | k < tk    = Tree tk tv (delete k left) right
                                 | k > tk    = Tree tk tv left (delete k right)
                                 | otherwise = case left of Empty -> let (Just mk, Just mv, rem_right) = extract_min right
                                                                     in Tree mk mv left rem_right
                                                            _     -> let (Just mk, Just mv, rem_left) = extract_max left
                                                                     in Tree mk mv rem_left right

