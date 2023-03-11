cd rgraphs
for f in *.dat
do  
    name=$(echo "$f" | cut -f 1 -d '.')
    echo $f
    echo time,expectedvalue,value,matching > ../rgraphs_execs/$name.csv
    for i in {1..30}
    do
        pypy3 ../fast_and_furious.py --max=True --value=False < $f >> ../rgraphs_execs/$name.csv
    done
done