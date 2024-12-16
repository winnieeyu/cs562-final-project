# CS562 Project Demo
By Team Mochi (Lauren Espineli and Winnie Yu)

## Instructions 
1. Download the files from Github 
2. Go to ```generator.py``` and on ```line 1210``` enter your PostgreSQL username and password
3. Next, on ```line 36``` input your desired .txt file. 
&emsp;(Reference "How to Properly Format Your Input" if you're having trouble)
4. Finally, run your code! 


### How to Properly Format Your Input 
1. Make sure you have your input as a .txt file 
2. The file only takes in 5 lines of the phi operands:
<br /> &emsp; S: List of projected attributes
<br /> &emsp; n: Number of grouping variables
<br /> &emsp; V: List of grouping attributes
<br /> &emsp; F: List of sets of aggregate functions
<br /> &emsp; o = List of predicates for grouping variables 
3. Only put in the values on separate lines, no need to put in the variables (i.e. "S=", "F=") 
4. Example Input:
```
prod, month, sum(1.quant), avg(2.quant) 
2 
prod, month 
sum(1.quant), avg(2.quant) 
1.prod=prod and month=month; 2.prod=prod
```

### Other Notes
- Make sure it's a .txt file and verify the correct file path
- Don't put additional spaces
