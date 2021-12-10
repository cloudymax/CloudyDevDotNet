# Code Tests

Random code challenges I've had to take or debug

### Password checker

- checks passwords strings for multiple conditions that would result in weak passwords. (30 minute timer)

    ??? Example "Code"
    
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

### Bean Finder

- Checks a list of integers and finds the smallest positive sequential integer missing from the set (30 minute timer)

    ??? Example "Code"

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

### Counting Vallies

- Debugging a faulty HackerRank question.

    ??? Example "Code"
    
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

        class Solution {

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

        	public static bool in_valley {

        		get {
        			return In_Valley;
        		}

        		set {
        			if (In_Valley) {
        				In_Valley = value;
        			}
        			else {
        				In_Valley = value;
        			};
        		}
        	}

        	//length of the current valley
        	public static int current_valley_length = 0;

        	// Complete the countingValleys function below.
        	static int countingValleys(int n, string s) {

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
        		foreach(char step in steps) {

        			counter += 1;

        			// process the steps
        			if (step.Equals('D')) {
        				altitude_current -= 1;
        			}

        			if (step.Equals('U')) {
        				altitude_current += 1;
        			}

        			if (altitude_last == 0 && altitude_current == -1) {
        				//we just stepped into a valley
        				in_valley = true;
        			}

        			if (altitude_last == -1 && altitude_current == 0) {
        				// back above sea level
        				if (current_valley_length >= min_valley_length) {
        					total_vallies += 1;
        					Console.WriteLine("Exited a Valley!");
        				}

        				in_valley = false;
        			}

        			//track valley length
        			if (in_valley) {
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

        	static void Main(string[] args) {
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

### Tile Time

> Link to Repo [Here](https://github.com/deserializeme/Game-Projects/blob/main/TileTime/README.md)

- One of the weirdest I've had to do (1 week take-home)

    1. The Rectangle_problem

        > Scene where given a point in 2d space, determine the closest point on a rect and the distance to 2d point. 
    
        > returns 0 if that point is inside the rect. Not allowed to use Unity's physics or colliders system.

        ??? Tip "Features"
            - Visual debugging! Test a point by left clicking
            - Enable the "every frame" option to test the mouse-position in real-time
            - Disable the "draw gizmos" option to test w/out visuals for performance tuning
            - in editor you can change the scale and location of the rect for more thorough testing.

        ??? Bug "known limitations"

            - only supports 4-sided shapes (as defined by reqs, but I can do square AND rectangles so thats a feature addition lol)
            - can't change individual points of the rect since its a hard-coded rect based on the min/max x/y values (Height = Length/2)
            - side detection breaks if rect has a negative scale, so the value is a range starting at 1, you dont need a negative scale rect, so im not worried about it
            - intersection point detection precision could be higher, but seems unecessary for this use case.

        <figure markdown> <!--  -->
          ![Dummy image](https://github.com/deserializeme/Game-Projects/blob/main/media/gifs/tiletime.gif?raw=true)
          <figcaption>Trigger/Edge detection</figcaption>
        </figure>

    - Tile Preview Problem

        > Creation of a custom Editor to fulfil requests from hypothetical designers requests

        </br>
        <figure markdown> <!--  -->
        ![Dummy image](https://github.com/deserializeme/Game-Projects/blob/main/media/images/custom-editor.PNG?raw=true)
        <figcaption>World Tile Editor</figcaption>
        </figure>

    - Scripts that make it work:  

        1. __click_for_point.cs__ 

            > handles getting your mouse position

            ??? Example "code"
            
                ```csharp
                using System.Collections;
                using System.Collections.Generic;
                using UnityEngine;

                namespace MouseInput
                {
                    public class click_for_point : MonoBehaviour
                    {
                        public static Vector3 get_mouse_position(Vector3 last_click_pos)
                        {
                            Vector3 click_position = last_click_pos;
                            Vector3 raw_mouse_position = Input.mousePosition;
                            Vector3 mouse_position = Camera.main.ScreenToWorldPoint(raw_mouse_position);
                            mouse_position.z = 0;

                            if (mouse_position != click_position)
                            {
                                click_position = mouse_position;
                            }

                            return click_position;
                        }
                    }
                }

                ```

        - __find_intersection.cs__ 

            > math library of static functions to handle to heavy vector math work. Again, they wont let you use the unity built-ins for this for some reason.

            ??? Example "code"

                ```csharp
                using System.Collections.Generic;
                using UnityEngine;

                namespace MathStuff
                {
                    public class find_intersection : MonoBehaviour
                    {
                        //sides of the rect as enums
                        public enum side
                        {
                            right, 
                            left,
                            top,
                            bottom,
                            inside
                        }

                        #region find the line intersection with the closest side of the rect
                        //math stuff 
                        // formula of a line: Ax + By = C
                        // A = Y1 - Y0
                        // B = X0 - X1
                        // C = Ax0 + By0
                        // we know (x0, y0),(x1, y1) for line segment 0 *the closest side to the point
                        // we know (x0, y0) for line segment 1, we need to find the direction towards the nearest side and the distance
                        // the shortest distance between 2 points is a straight line, so we can just use right angles which make sit simpler
                        /// <summary>
                        /// Returns the Vector3 of the closest point on the rect
                        /// </summary>
                        /// <param name="point">A vector3.</param>
                        /// <param name="my_rect">A RectMaker.Rect.</param>
                        public static KeyValuePair<bool, Vector3> Intersection_Point(Vector3 test_point, RectMaker.Rect my_rect)
                        {
                            //get the closest side
                            side closest_side;
                            closest_side = NearSide(test_point, my_rect);

                            #region hold points of our rect
                            Vector3 p0 = new Vector3(my_rect.minX, my_rect.minY, 0) + my_rect.center;
                            Vector3 p1 = new Vector3(my_rect.minX, my_rect.maxY, 0) + my_rect.center;
                            Vector3 p2 = new Vector3(my_rect.maxX, my_rect.maxY, 0) + my_rect.center;
                            Vector3 p3 = new Vector3(my_rect.maxX, my_rect.minY, 0) + my_rect.center;
                            #endregion

                            #region initialize some variables
                            Vector3 intersection_location = Vector3.zero;
                            bool is_on_line = false;
                            Vector3 seg1_dir = Vector3.zero;
                            Vector3 seg1_start = test_point;
                            Vector3 difference = Vector3.zero;
                            float single_axis_distance = 0;
                            float seg0_A = 0;
                            float seg0_B = 0;
                            float seg0_C = 0;
                            Vector3 side_start = p0;
                            Vector3 side_end = p0;
                            #endregion

                            //chose the direction based on the returned side, then get the single axis distance
                            // kind of cheating but acceptance criteria said shortest distance.        
                            #region handle each side of the rect
                            if (closest_side == side.left)
                            {
                                side_start = p0;
                                side_end = p1;

                                seg1_dir = Vector3.right;
                                difference = side_start - test_point;
                                single_axis_distance = Mathf.Abs(difference.x);
                            }

                            if (closest_side == side.top)
                            {
                                side_start = p1;
                                side_end = p2;

                                seg1_dir = -Vector3.up;
                                difference = side_start - test_point;
                                single_axis_distance = Mathf.Abs(difference.y);
                            }

                            if (closest_side == side.right)
                            {
                                side_start = p2;
                                side_end = p3;

                                seg1_dir = -Vector3.right;
                                difference = side_start - test_point;
                                single_axis_distance = Mathf.Abs(difference.x);
                            }

                            if (closest_side == side.bottom)
                            {
                                side_start = p3;
                                side_end = p0;

                                seg1_dir = Vector3.up;
                                difference = side_start - test_point;
                                single_axis_distance = Mathf.Abs(difference.y);
                            }
                            #endregion

                            //get our lines in the proper format
                            seg0_A = side_end.y - side_start.y;
                            seg0_B = side_start.x - side_end.x;
                            seg0_C = ((seg0_A * side_start.x) + (seg0_B * side_start.y));

                            //now that we have the direction and distance for the last line segment we can get the interseation point
                            intersection_location = seg1_start + (seg1_dir.normalized * single_axis_distance);


                            KeyValuePair<bool, Vector3> test = On_Line(side_start, side_end, seg1_dir, intersection_location);
                            if (!test.Key)
                            {
                                intersection_location = test.Value;
                                is_on_line = false;
                            }
                            else
                            {
                                is_on_line = true;
                            }

                            KeyValuePair<bool, Vector3> results = new KeyValuePair<bool, Vector3>(is_on_line, intersection_location);

                            return results;
                        }
                        #endregion

                        #region is intersection point on a line segment and if not, return closest end of the line segment
                        public static KeyValuePair<bool, Vector3> On_Line(Vector3 seg_start, Vector3 seg_end, Vector3 seg_direction, Vector3 test_point)
                        {
                            bool is_on_segment = false;
                            Vector3 closest_point;

                            float segment = Mathf.Sqrt(
                                (seg_end.x - seg_start.x) * (seg_end.x - seg_start.x) 
                                + (seg_end.y - seg_start.y) * (seg_end.y - seg_start.y) 
                                + (seg_end.z - seg_start.z) * (seg_end.z - seg_start.z)
                                );

                            float start_to_point = Mathf.Sqrt(
                                (test_point.x - seg_start.x) * (test_point.x - seg_start.x)
                                + (test_point.y - seg_start.y) * (test_point.y - seg_start.y)
                                + (test_point.z - seg_start.z) * (test_point.z - seg_start.z));

                            float point_to_end = Mathf.Sqrt(
                                (seg_end.x - test_point.x) * (seg_end.x - test_point.x)
                                + (seg_end.y - test_point.y) * (seg_end.y - test_point.y)
                                + (seg_end.z - test_point.z) * (seg_end.z - test_point.z));

                            //Debug.Log("segent: " + segment + " start-to-point: " + start_to_point + " point-to-end: " + point_to_end);
                            //Debug.Log("segent: " + segment + " vs start-to-point + point-to-end: " + Mathf.Abs(start_to_point + point_to_end));

                            //low precision, could get this lower with more time to test but it passes all the tests im throwing at it
                            if(Mathf.Abs(segment - (start_to_point + point_to_end)) < .5f )
                            {
                                is_on_segment = true;
                                closest_point = test_point;
                            }
                            else
                            {
                                if(start_to_point > point_to_end)
                                {
                                    closest_point = seg_end;
                                }
                                else
                                {
                                    closest_point = seg_start;
                                }
                            }

                            KeyValuePair<bool, Vector3> results = new KeyValuePair<bool, Vector3>(is_on_segment, closest_point);

                            //Debug.Log(is_on_segment);
                            return results;
                        }

                        #endregion

                        #region find the closest side of the rect to an outside point
                        /// <summary>
                        /// Returns the name of the nearest side of the rect to the supplied Vector3 point as an Enum
                        /// </summary>
                        /// <param name="point">A vector3.</param>
                        /// <param name="my_rect">A RectMaker.Rect.</param>
                        public static side NearSide(Vector3 point, RectMaker.Rect my_rect)
                        {
                            side nearest_side = side.inside;

                            if(!InsideClick(point, my_rect))
                            {
                                if (point.x > my_rect.maxX + my_rect.center.x)
                                {
                                    //right
                                    nearest_side = side.right;
                                }

                                if (point.x < my_rect.minX + my_rect.center.x)
                                {
                                    //left
                                    nearest_side = side.left;
                                }

                                if (point.y > my_rect.maxY + my_rect.center.y)
                                {
                                    //above
                                    nearest_side = side.top;
                                }

                                if (point.y < my_rect.minY + my_rect.center.y)
                                {
                                    //below
                                    nearest_side = side.bottom;
                                }
                            }


                            return nearest_side;
                        }
                        #endregion 

                        #region Is the point inside the rect? 
                        /// <summary>
                        /// Returns true if point is inide rect, and false if it is outside the rect.
                        /// </summary>
                        /// <param name="point">A vector3.</param>
                        /// <param name="my_rect">A RectMaker.Rect.</param>
                        public static bool InsideClick(Vector3 point, RectMaker.Rect my_rect)
                        {
                            bool inside = true;

                            if (point.x > my_rect.maxX + my_rect.center.x)
                            {
                                //right
                                inside = false;
                            }

                            if (point.x < my_rect.minX + my_rect.center.x)
                            {
                                //left
                                inside = false;
                            }

                            if (point.y > my_rect.maxY + my_rect.center.y)
                            {
                                //above
                                inside = false;
                            }

                            if (point.y < my_rect.minY + my_rect.center.y)
                            {
                                //below
                                inside = false;
                            }

                            return inside;
                        }
                        #endregion

                    }

                }
                ```

        - __rect_maker.cs__ 

            > struct that defines the rect we will be testing with as defined in requirements, added a couple fields because i make my own destiny.

            ??? Example "code"
                ```csharp
                using UnityEngine;

                namespace RectMaker
                {
                    public struct Rect
                    {
                        public float scale;
                
                        public Color color;
                        public float minX;
                        public float minY;
                        public float maxX;
                        public float maxY;
                
                        public Vector3 center;
                
                        public Rect(float scale, Color color, Vector3 center)
                        {
                        
                            this.color = color;
                            
                            this.scale = scale;
                
                            this.center = center;
                
                            //directions say to make it a rectangle, so we're making it a rectangle
                
                            // DEF: a plane figure with four straight sides and four right angles, 
                            //especially one with unequal adjacent sides, in contrast to a square.
                            this.minX = 0 - this.scale;
                            this.minY = 0 - this.scale/2;
                            this.maxX = 0 + this.scale;
                            this.maxY = 0 + this.scale/2;
                        }
                    };
                
                }

                ```

        - __rect_manager.cs__ 

            > manages the rect, mouse position, and most of the core loop. serves as our link to other scripts (namely the UI)

            ??? Example "code"
                ```csharp
                using MouseInput;
                using System.Collections.Generic;
                using UnityEngine;
                using MathStuff;
                
                [RequireComponent(typeof(click_for_point))]
                public class rect_manager : MonoBehaviour
                {
                
                    #region variables
                    //draw handles for a visual representation of the problem
                    public bool draw_debug = true;
                    public bool every_frame = false;
                
                    //the rect we will be testing
                    public RectMaker.Rect my_rect;
                
                    //the size of the rect
                    [Range(1f, 50f)]
                    public float rect_scale = 25f;
                
                    //side of the handles 
                    [Range(1f, 10f)]
                    public float handle_scale = 1f;
                
                    //center point of the rect
                    public Vector3 rect_center;
                
                    //color to draw the rect, using collider green becaue we're basically remaking the 2d collider system at this point so why not
                    public Color rect_color = Color.green;
                
                
                    //if we have made an initial click or not, just hides the handle until we have valid input
                    bool clicked = false;
                
                    //position to test
                    public Vector3 click_position;
                    public Vector3 intersection_point;
                
                    public float distance_from_click;
                    public bool click_is_inside_rect;
                
                
                    #region points to draw
                    // vector3s we create from the RectMaker.Rect's min/max X/Y and scale
                    Vector3 p0;
                    Vector3 p1;
                    Vector3 p2;
                    Vector3 p3;
                    Vector3 handle_size;
                    #endregion
                
                    #endregion
                
                    #region unity methods
                    void Start()
                    {
                        rect_center = Vector3.zero;
                        click_position = Vector3.zero;
                        NewRect();
                    }
                
                    void Update()
                    {
                        if(every_frame)
                        {
                            click_position = click_for_point.get_mouse_position(click_position);
                            Check_conditions();
                        }
                        else
                        {
                            Check_For_Input();
                        }
                
                        Update_Points();
                    }
                
                    void OnDrawGizmos()
                    {
                        if (draw_debug)
                        {
                            if (Application.isPlaying)
                            {
                                Internal_Point();
                                Draw_Handles();
                                Draw_Rect_Lines();
                                Draw_Intersection();
                            }
                        }
                    }
                
                    #endregion
                
                    #region custom methods
                    void Check_For_Input()
                    {
                        if (Input.GetMouseButtonDown(0))
                        {
                            click_position = click_for_point.get_mouse_position(click_position);
                
                            if (!clicked)
                            {
                                clicked = true;
                            }
                
                            Check_conditions();
                        }
                    }
                
                    void Check_conditions()
                    {
                        KeyValuePair<bool, Vector3> results;
                        click_is_inside_rect = find_intersection.InsideClick(click_position, my_rect);
                
                        if (!click_is_inside_rect)
                        {
                            results = find_intersection.Intersection_Point(click_position, my_rect);
                            if(results.Key)
                            {
                                intersection_point = results.Value;
                            }
                
                            distance_from_click = Vector3.Distance(click_position, intersection_point);
                        }
                        else
                        {
                            distance_from_click = 0;
                        }
                    }
                
                    void Update_Points()
                    {
                        //update the scale if we want to
                        if (my_rect.scale != rect_scale)
                        {
                            NewRect();
                        }
                
                        //update the position if we want to
                        if (my_rect.center != rect_center)
                        {
                            NewRect();
                        }
                
                        //update the color if we want to
                        if (my_rect.color != rect_color)
                        {
                            NewRect();
                        }
                
                        //update handle sizes live
                        handle_size = new Vector3(handle_scale, handle_scale, handle_scale);
                    }
                
                    void NewRect()
                    {
                        my_rect = new RectMaker.Rect(rect_scale, rect_color, rect_center);
                        p0 = new Vector3(my_rect.minX, my_rect.minY, 0) + rect_center;
                        p1 = new Vector3(my_rect.minX, my_rect.maxY, 0) + rect_center;
                        p2 = new Vector3(my_rect.maxX, my_rect.maxY, 0) + rect_center;
                        p3 = new Vector3(my_rect.maxX, my_rect.minY, 0) + rect_center;
                    }
                
                    void Internal_Point()
                    {
                        if (find_intersection.InsideClick(click_position, my_rect))
                        {
                            Gizmos.color = Color.red;
                        }
                        else
                        {
                            Gizmos.color = Color.white;
                        }
                
                        if (clicked && !every_frame)
                        {
                            Gizmos.DrawCube(click_position, handle_size);
                        }
                        else
                        {
                            if (every_frame)
                            {
                                Gizmos.DrawCube(click_position, handle_size);
                            }
                        }
                    }
                
                    void Draw_Handles()
                    {
                        Gizmos.color = my_rect.color;
                        //bottom left
                        Gizmos.DrawCube(p0, handle_size);
                        //top left
                        Gizmos.DrawCube(p1, handle_size);
                        //top right
                        Gizmos.DrawCube(p2, handle_size);
                        //bottom right
                        Gizmos.DrawCube(p3, handle_size);
                
                        Gizmos.DrawCube(rect_center, handle_size);
                    }
                
                    void Draw_Rect_Lines()
                    {
                        #region default rect
                        Gizmos.color = rect_color;
                        Gizmos.DrawLine(p0, p1);
                        Gizmos.DrawLine(p1, p2);
                        Gizmos.DrawLine(p2, p3);
                        Gizmos.DrawLine(p3, p0);
                        #endregion
                
                        find_intersection.side side = find_intersection.NearSide(click_position, my_rect);
                
                        if (side == find_intersection.side.left)
                        {
                            #region draw left side red, all others rect_color
                            Gizmos.color = Color.red;
                            Gizmos.DrawLine(p0, p1);
                
                            Gizmos.color = rect_color;
                            Gizmos.DrawLine(p1, p2);
                            Gizmos.DrawLine(p2, p3);
                            Gizmos.DrawLine(p3, p0);
                            #endregion
                        }
                
                        if (side == find_intersection.side.top)
                        {
                            #region draw top side red, all others rect_color
                            Gizmos.color = Color.red;
                            Gizmos.DrawLine(p1, p2);
                
                            Gizmos.color = rect_color;
                            Gizmos.DrawLine(p0, p1);
                            Gizmos.DrawLine(p2, p3);
                            Gizmos.DrawLine(p3, p0);
                            #endregion
                        }
                
                        if (side == find_intersection.side.right)
                        {
                            #region draw right side red, all others rect_color
                            Gizmos.color = Color.red;
                            Gizmos.DrawLine(p2, p3);
                
                            Gizmos.color = rect_color;
                            Gizmos.DrawLine(p0, p1);
                            Gizmos.DrawLine(p1, p2);
                            Gizmos.DrawLine(p3, p0);
                            #endregion
                        }
                
                        if (side == find_intersection.side.bottom)
                        {
                            #region draw bottom side red, all others rect_color
                            Gizmos.color = Color.red;
                            Gizmos.DrawLine(p3, p0);
                
                            Gizmos.color = rect_color;
                            Gizmos.DrawLine(p0, p1);
                            Gizmos.DrawLine(p1, p2);
                            Gizmos.DrawLine(p2, p3);
                            #endregion
                        }
                    }
                
                    void Draw_Intersection()
                    {
                        KeyValuePair<bool, Vector3> results;
                
                        if (!find_intersection.InsideClick(click_position, my_rect))
                        {
                            results = find_intersection.Intersection_Point(click_position, my_rect);
                
                            intersection_point = results.Value;
                            Gizmos.color = Color.red;
                            Gizmos.DrawCube(intersection_point, handle_size);
                            Gizmos.DrawLine(click_position, intersection_point);
                        }
                    }
                    #endregion
                }
                ```

        - __ui_manager.cs__

            > pulls values from rect_manager.cs to drive a small UI.

            ??? Example "Code"

                ```csharp
                using UnityEngine;
                using TMPro;
                using UnityEngine.UI;

                [RequireComponent(typeof(rect_manager))]
                public class ui_manager : MonoBehaviour
                {
                    public TextMeshProUGUI distance_value;
                    public TextMeshProUGUI point_value;
                    public TextMeshProUGUI i_point_value;
                    public TextMeshProUGUI inside_value;
                    public Toggle frame_toggle;
                    public Toggle gizmo_toggle;


                    private float _distance;
                    float distance
                    {
                        get
                        {
                            return _distance;
                        }

                        set
                        {
                            _distance = value;
                            distance_value.SetText("{0:2}", _distance);
                        }
                    }

                    private Vector3 _pos;
                    Vector3 pos
                    {
                        get
                        {
                            return _pos;
                        }

                        set
                        {
                            _pos = value;
                            point_value.SetText("( {0:1}, {1:1}, {2:1} )", rm.click_position.x, rm.click_position.y, rm.click_position.z);
                        }
                    }

                    private Vector3 _ipos;
                    Vector3 ipos
                    {
                        get
                        {
                            return _ipos;
                        }

                        set
                        {
                            _ipos = value;
                            i_point_value.SetText("( {0:1}, {1:1}, {2:1} )", rm.intersection_point.x, rm.intersection_point.y, rm.intersection_point.z);
                        }
                    }

                    private bool _inside;
                    bool inside
                    {
                        get
                        {
                            return _inside;
                        }

                        set
                        {
                            _inside = value;
                            inside_value.SetText(rm.click_is_inside_rect.ToString());
                        }
                    }

                    rect_manager rm;

                    void Start()
                    {
                        rm = gameObject.GetComponent<rect_manager>();
                        inside = rm.click_is_inside_rect;
                    }

                    void Update()
                    {
                        compare_values();
                    }

                    void compare_values()
                    {
                        if(distance != rm.distance_from_click)
                        {
                            distance = rm.distance_from_click;
                        }

                        if(pos != rm.click_position)
                        {
                            pos = rm.click_position;
                        }

                        if (ipos != rm.intersection_point)
                        {
                            ipos = rm.intersection_point;
                        }

                        if (inside != rm.click_is_inside_rect)
                        {
                            inside = rm.click_is_inside_rect;
                        }

                        if(rm.every_frame != frame_toggle.isOn)
                        {
                            rm.every_frame = frame_toggle.isOn;
                        }

                        if(rm.draw_debug != gizmo_toggle.isOn)
                        {
                            rm.draw_debug = gizmo_toggle.isOn;
                        }

                    }

                }
                ```
   
        - __world_tile_editor.cs__

            > Editor for manipulating custom class

            ??? Example "Code"

                ```csharp
                using UnityEngine;
                using System.Collections;
                using UnityEditor;
                using System.Collections.Generic;
                using System.IO;
                using UnityEngine.UI;
                using System.Linq;
                using UnityEditor.PackageManager.UI;

                [CustomEditor(typeof(WorldTile))]
                public class world_tile_editor : Editor
                {
                    public WorldTile my_tile;
                    string enemy_weight;
                    string level_weight;

                    public override void OnInspectorGUI()
                    {
                        my_tile = (WorldTile)target;

                        //initialize the sprite if non exists
                        if(!my_tile.tileSprite)
                        {
                            DirectoryInfo dir = new DirectoryInfo("Assets/Resources/Sprites/Tile");
                            FileInfo[] info = dir.GetFiles("*.png");
                            my_tile.tileSprite = (Sprite)AssetDatabase.LoadAssetAtPath("Assets/Resources/Sprites/Tile/" + info[0].Name, typeof(Sprite));
                        }

                        //nasty regex to get the constants out of the world tile
                        #region
                        DirectoryInfo mydir = new DirectoryInfo("Assets/Scripts");
                        FileInfo[] fi = mydir.GetFiles("*.cs");
                        foreach (FileInfo f in fi)
                        {
                            if (f.Name == "WorldTile.cs")
                            {
                                string result = string.Empty;
                                var lines = File.ReadAllLines(f.FullName);
                                foreach (var line in lines)
                                {
                                    if (line.Contains("public const float ENEMY_WEIGHT ="))
                                    {
                                        enemy_weight = System.Text.RegularExpressions.Regex.Replace(line, "public const float ENEMY_WEIGHT =", "");
                                        enemy_weight = enemy_weight.Trim(' ', ';', 'f');
                                    }

                                    if (line.Contains("public const float LEVEL_WEIGHT"))
                                    {
                                        level_weight = System.Text.RegularExpressions.Regex.Replace(line, "public const float LEVEL_WEIGHT =", "");
                                        level_weight = level_weight.Trim(' ', ';', 'f');
                                    }
                                }
                            }
                        }
                        #endregion


                        //sprite selection
                        #region 
                        Texture tex = AssetPreview.GetAssetPreview(my_tile.tileSprite);

                        //title
                        EditorGUILayout.BeginHorizontal("TextArea");
                        EditorGUILayout.LabelField("Curret Sprite Selection: " + my_tile.tileSprite.name, EditorStyles.boldLabel);
                        EditorGUILayout.EndHorizontal();

                        //button and preview
                        EditorGUILayout.BeginHorizontal("Box");
                        EditorGUILayout.BeginVertical();
                        if (GUILayout.Button("change sprite", GUILayout.ExpandWidth(true)))
                        {
                            //create a popup
                            MyWindow.Init(my_tile);
                        }
                        EditorGUILayout.EndVertical();
                        GUILayout.Label(tex);
                        EditorGUILayout.EndHorizontal();
                        #endregion


                        //Difficulty Settings
                        #region
                        //title

                        EditorGUILayout.BeginVertical("TextArea");
                        EditorGUILayout.LabelField("Difficulty Level: " + my_tile.CalculateDifficulty(), EditorStyles.boldLabel);
                        EditorGUILayout.EndVertical();

                        EditorGUILayout.BeginVertical("Box");
                        EditorGUILayout.BeginHorizontal("Box");
                        EditorGUILayout.LabelField("enemy & level weights: (" + enemy_weight + " / " + level_weight+ ")");
                        EditorGUILayout.EndHorizontal();

                        //level setting
                        #region
                        //title
                        EditorGUILayout.BeginHorizontal("Box");
                        EditorGUILayout.LabelField("Tile Level: " + my_tile.level, EditorStyles.boldLabel);
                        EditorGUILayout.EndHorizontal();

                        //Slider
                        my_tile.level = EditorGUILayout.IntSlider(my_tile.level, 1, 25);
                        #endregion

                        //Enemy Count setting
                        #region
                        //title
                        EditorGUILayout.BeginHorizontal("Box");
                        EditorGUILayout.LabelField("Number of Enemies: " + my_tile.numEnemies, EditorStyles.boldLabel);
                        EditorGUILayout.EndHorizontal();

                        //Slider
                        my_tile.numEnemies = EditorGUILayout.IntSlider(my_tile.numEnemies, 1, 500);
                        #endregion

                        EditorGUILayout.EndVertical();
                        #endregion


                        //save a prefab
                        #region
                        //title and text iput
                        EditorGUILayout.BeginHorizontal("TextArea");
                        if (GUILayout.Button("Save as prefab", GUILayout.ExpandWidth(true)))
                        {
                            SaveWindow.Init(my_tile);
                        }
                        EditorGUILayout.EndHorizontal();
                        #endregion




                        if (GUI.changed)
                        {
                            EditorUtility.SetDirty(my_tile);
                        }
                    }
                }

                public class MyWindow : EditorWindow
                {
                    public List<Sprite> sprites = new List<Sprite>();
                    public Texture[] textures; 
                    public WorldTile my_tile;
                    int selGridInt = 0;

                    public static void Init(WorldTile tile)
                    {
                        // Get existing open window or if none, make a new one:
                        MyWindow window = (MyWindow)EditorWindow.GetWindow(typeof(MyWindow));
                        window.my_tile = tile;
                        window.Show();
                    }

                    void OnGUI()
                    {
                        //populate the sprites
                        Sprite_Field(my_tile);

                        //create a selection grid
                        selGridInt = GUILayout.SelectionGrid(selGridInt, textures, 4);

                        if (GUILayout.Button("select"))
                        {
                            my_tile.tileSprite = sprites[selGridInt];
                            this.Close();
                        }


                    }

                    void Sprite_Field(WorldTile my_tile)
                    {
                        //load all our sprites from the folder we want to use
                        DirectoryInfo dir = new DirectoryInfo("Assets/Resources/Sprites/Tile");
                        FileInfo[] info = dir.GetFiles("*.png");
                        foreach (FileInfo f in info)
                        {
                            Sprite my_sprite = (Sprite)AssetDatabase.LoadAssetAtPath("Assets/Resources/Sprites/Tile/" + f.Name, typeof(Sprite));
                            if (!sprites.Contains(my_sprite))
                            {
                                sprites.Add(my_sprite);
                            }
                        }

                        //setup an array because we have to give the selection grid the data type it wants
                        textures = new Texture[sprites.Count];
                        for(int i = 0; i < sprites.Count; i++)
                        {
                            textures[i] = sprites[i].texture;
                        }
                    }
                }


                public class SaveWindow : EditorWindow
                {
                    public WorldTile my_tile;
                    public string prefab_name = "Enter Name";

                    public static void Init(WorldTile tile)
                    {
                        SaveWindow window = (SaveWindow)EditorWindow.GetWindow(typeof(SaveWindow));
                        window.my_tile = tile;
                        window.Show();
                    }

                    void OnGUI()
                    {
                        prefab_name = GUILayout.TextField(prefab_name, 255);

                        if (GUILayout.Button("Save"))
                        {
                            PrefabUtility.SaveAsPrefabAsset(Selection.activeGameObject, "Assets/Resources/Sprites/Prefabs/" + prefab_name + ".prefab", out bool success);
                            this.Close();
                        }
                    }
                }
                ```
