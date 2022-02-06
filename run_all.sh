for (( i = 1; i <= 25; i++ )); do 
    n=$(printf "%02d" $i); 
    printf "\n\n\n   $n   \n--------\n"; 
    time python3 aoc$n.py ${n}_input; 
done
