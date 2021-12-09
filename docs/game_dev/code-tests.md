# Code Tests

Random code challenges I've had to take or debug

1. Password checker

    ```python
    #!/usr/bin/env python3
    some_string = "FooBar123!"
    def is_it_secure(some_string):
        print("must be longer than 6")
        if len(some_string) < 6:
            return False
        #break apart the string into chars
        char_list = list(some_string)
        print("must contain a special")
        special_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_']
        if not contains_special(char_list, special_chars):
            return False
        print("must container a upper")
        if not contains_upper(char_list):
            return False
        print("must container an int")
        if not contains_int(char_list):
            return False
        #finally
        print("no spaces allowed >:(")
        if contains_no_space(char_list):
            return True
        else:
            return False
    def contains_special(list_of_chars, special_chars):
        for char in list_of_chars:
            if char in special_chars:
                return True
        return False
    def contains_upper(list_of_chars):
    
        for char in list_of_chars:
            if char.isupper():
                return True
        return False
    def contains_int(list_of_chars):
        for char in list_of_chars:
            try:
                int(char)
                return True
            except:
                pass
        return False
    def contains_no_space(list_of_chars):
    
        for char in list_of_chars:
            if char.isspace():
                return False
        return True
    print(is_it_secure(some_string))
    ```

2. Bean Finder

```python
#!/usr/env python3

    def smol_finder(beans):
        """
        Takes an input of type Array containing Integers.
        Dedups, then returns the smollest bean
        """

        # dedups our input
        cool_beans = sorted(set(beans))


        # print our cool bean list
        print(f"Check out these beans: {cool_beans}")

        # show the smollest bean
        smollest = int(list(cool_beans)[0])
        print(f"the smollest bean is {smollest}")

        # show the lorgest bean
        lorgest = int(list(cool_beans)[-1])
        print(f"the lorgest bean is {lorgest}")

        if lorgest < 1:
            return 1

        range_end = lorgest + 1
        x = range(smollest, range_end)
        for number in x:
            if number not in cool_beans:
                return number


    bean_array = [1,3,6,4,1,2]

    my_smollest_bean = smol_finder(bean_array)

    print(f"this is the smollest positive int missing from my beans:    {my_smollest_bean}")    


    ``` 

3. Counting Vallies

        ```csharp
        using System.CodeDom.Compiler;
        using System.Collections.Generic;
        using System.Collections;
        using System.ComponentModel;
        using System.Diagnostics.CodeAnalysis;
        using System.Globalization;
        using System.IO;
        using System.Linq;
        using System.Reflection;
        using System.Runtime.Serialization;
        using System.Text.RegularExpressions;
        using System.Text;
        using System;

        class Solution
        {
        
            //step history
            public static char[] steps;

            //current altitude at end of step
            public static int altitude_current = 0;

            //altitude at start of step
            public static int altitude_last = 0;

            //total valleys
            public static int total_vallies = 0;

            //if we are in a valley right now
            private static bool In_Valley;

            //test case for "consecutive steps"
            public static int min_valley_length = 2;

            public static bool in_valley
            {
            
                get
                {
                    return In_Valley;
                }

                set
                {
                    if (In_Valley)
                    {
                        In_Valley = value;
                    }
                    else
                    {
                        In_Valley = value;
                    };
                }
            }

            //length of the current valley
            public static int current_valley_length = 0;

            // Complete the countingValleys function below.
            static int countingValleys(int n, string s)
            {
            
                //step history, new each time
                steps = s.ToCharArray();

                //current altitude at end of step, reset this value
                altitude_current = 0;

                //altitude at start of step, reset this value 
                altitude_last = 0;

                //if we are in a valley, track the progress
                current_valley_length = 0;

                int counter = 0;

                in_valley = false;


                //process step history
                //the step back history if you will =P
                foreach (char step in steps)
                {
                
                    counter += 1;

                    // process the steps
                    if (step.Equals('D'))
                    {
                        altitude_current -= 1;
                    }

                    if (step.Equals('U') )
                    {
                        altitude_current += 1;
                    }

                    if (altitude_last == 0 && altitude_current == -1)
                    {
                        //we just stepped into a valley
                        in_valley = true;
                    }

                    if (altitude_last == -1 && altitude_current == 0)
                    {
                        // back above sea level
                        if(current_valley_length >= min_valley_length)
                        {
                            total_vallies += 1;
                            Console.WriteLine("Exited a Valley!");
                        }

                        in_valley = false;
                    }

                    //track valley length
                    if (in_valley)
                    {
                        current_valley_length += 1;
                    }

                    Console.WriteLine("------------------------------------------------------------------------");
                    Console.WriteLine("step: " + counter + "processed. Value is: " + step);
                    Console.WriteLine("Current Altitude: " + altitude_current);
                    Console.WriteLine("Previous Altitude: " + altitude_last);
                    Console.WriteLine("In Valley? : " + in_valley + "| Valley Length: " + current_valley_length);
                    Console.WriteLine("Total Vallies Discovered: " + total_vallies);

                    //store the last altitude
                    altitude_last = altitude_current;

                }

                return total_vallies;
            }




            static void Main(string[] args)
            {
                TextWriter textWriter = new StreamWriter(@System.Environment.GetEnvironmentVariable("OUTPUT_PATH"), true);

                int n = Convert.ToInt32(Console.ReadLine());

                string s = Console.ReadLine();

                int result = countingValleys(n, s);

                textWriter.WriteLine(result);

                textWriter.Flush();
                textWriter.Close();
            }
        }

        ```