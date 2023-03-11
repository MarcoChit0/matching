cd data
for f in *.dat
do  
    name=$(echo "$f" | cut -f 1 -d '.')
    echo time,expectedvalue,value,matching > ../execs/$name.csv
    for i in {1..30}
    do
        pypy3 ../fast_and_furious.py --min=True < $f >> ../execs/$name.csv
    done
done