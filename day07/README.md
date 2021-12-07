# [Day 7: The Treachery of Whales](https://adventofcode.com/2021/day/7)

I didn't solve this one with brute force, but my mathematical background was not strong enough.
I googled for a minimization of deltas from data to a value, and found some articles explaining the difference
between mean and median.

In french sorry:
- [Et si on s’intéressait à la moyenne des écarts ?](https://www.apmep.fr/IMG/pdf/AAA14048.pdf)
- [Calcul de la médiane](https://www150.statcan.gc.ca/n1/edu/power-pouvoir/ch11/median-mediane/5214872-fra.htm)

The first one states "The median minimizes the deltas"... Here we are, part 1 will be solved by computing the median 
value. Next challenge was not to sort the whole data, but to work with a cumulative frequency histogram, looking for the
first value reaching half the total number of values.

I secretly hoped that part 2 would work as well, changing only the fuel consumption method. Ooops, reading carefully the
challenge showed that the optimal value was also changing and should be computed differently. I let the problem mature 
for a few hours...

Part 2 fuel consumption is a classic running sum `1 + 2 + 3 + 4 + ... + k` which equals to `k * (k + 1) / 2`. k * k is a 
square (wow!) and I read in the papers that the mean mas minimizing the delta squares... Here we are for part 2.

But unlike median which is a number taken in the data, mean is a computation and gives a decimal result in our case. 
So I tried with the two surrounding integers and chose the one which was giving the lowest total consumption.

I'm not fully satisfied with part 2 solution because it's not strongly designed with mathematics, but resides in a 
lucky feeling attempt ;-)

By the way, no Python trick in this solution except classic itertools, but a real maths challenge.

Loved this one later:
[On the Unreasonable Efficacy of the Mean in Minimizing the Fuel Expenditure of Crab 
Submarines](https://www.reddit.com/r/adventofcode/comments/rawxad/2021_day_7_part_2_i_wrote_a_paper_on_todays/)
