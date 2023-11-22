array[1..5] of int: ar;
array[1..5, 1..4] of int: ar2;

var int: score;

constraint score = max([ar[y] | y in [ar2[1, x] | x in 1..4]]);

solve maximize score;

