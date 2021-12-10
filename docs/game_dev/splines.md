# Spline Tools

A novel system for crating animations and pathing using Splines/bezier curves in the Unity 3D engine. Originally developed to compliment the FOE MMO/MOBA combat systems. A version of the complete project is available [here](https://github.com/deserializeme/Game-Projects/tree/main/combat_system)

Huge thanks to [<u>Freya Holmer</u>](https://twitter.com/FreyaHolmer) for their incredible articles and presentations on [<u>bezier curves</u>](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjEnbzdxNn0AhWHy6QKHSCSCtsQFnoECAQQAQ&url=https%3A%2F%2Facegikmo.medium.com%2Fthe-ever-so-lovely-b%25C3%25A9zier-curve-eb27514da3bf&usg=AOvVaw1Pyw-ANRIhKRd8SHakKWkp) which heavily inspired this system. 

<figure markdown> <!--  -->
  ![Dummy image](https://raw.githubusercontent.com/cloudymax/Unity-References/main/Splines/custom_editors/editorviewsplineeditor.PNG)
  <figcaption>Editor view</figcaption>
</figure>

## Motivation

Inspired by this video-essay:
[How the fundamentals of animation apply to game design with League of Legends](https://www.youtube.com/watch?v=rXLH0nkgkbc)

!!! Warning
    
    Warning: depicts some anime violence - skip to 1:30 to bypass.

## Goals

1. Reduce difficulty prototyping complex ability interraction chains

- getting meaningful logging data

- Create tools to implement essential principles of animation in the movement of non-ambulatory actors

- Ability to randomly seed/generate abilities and animations to kick-start the creative process


    !!! Tip
      
        Special thanks to @FreyaHolmer's 2015 Unite presentation on the subject for being a fantastic primer.
    

## Examples


- "Justice rains from above..."

<figure markdown> <!--  -->
    <video autoplay loop muted src="https://thumbs.gfycat.com/FemaleFaithfulBorderterrier-mobile.mp4">
    </video>
  <figcaption>Recreating Pharah from Overwatch's Ultimate using random spline reflection</figcaption>
</figure>

- loopy loops

<figure markdown> <!--  -->
    <video autoplay loop muted src="https://thumbs.gfycat.com/ThoroughSeriousIchidna-mobile.mp4">
    </video>
  <figcaption>object showing the "orbit" option to rotate around the spline path, then switching to a direct flight path, then adding a status effect to the target</figcaption>
</figure>

- Editor and Game views
    
    ???+ Example 

        <figure markdown> <!--  -->
            <video autoplay loop muted src="https://thumbs.gfycat.com/HollowMajesticArmadillo-mobile.mp4">
            </video>
            <figcaption>Switching between the game and Editor views while an animation plays. This shows the custom editor gizmos created to help customize spline paths and animations</figcaption>
        </figure>

- Spline Manager Editor

    ??? Example
    
        ![Dummy image](../images/unity/editors-code-post/spline_manager.PNG)

- Spline Profile Editor

    ??? Example

        ![Dummy image](../images/unity/editors-code-post/spline_profile_viewer.PNG)

- Editor Gizmos in-scene

    ??? Example

        ![Dummy image](../images/unity/editors-code-post/editor_view.PNG)


## Maths

Heres what the math for all that looks like in code.

??? Example "Basic Spline"
  
    ```csharp
        // Basic
        // returns a vector3 point at <t> position on a spline
        public static Vector3 GetPoint(Vector3 p0, Vector3 p1, Vector3 p2, Vector3 p3, float t)
        {
            t = Mathf.Clamp01(t);
            float oneMinusT = 1f - t;
            return
                oneMinusT * oneMinusT * oneMinusT * p0 +
                3f * oneMinusT * oneMinusT * t * p1 +
                3f * oneMinusT * t * t * p2 +
                t * t * t * p3;
        }
    ```

??? Example "Advanced Spline"

    ```csharp
        // Advanced
        // return a point on a given spline at <t> based on several modfied behavior patterns.

        public static void TraverseSpline(GameObject Source, GameObject Target, CreateSplineProfile Spline, GameObject ObjectToMove, float T)
        {
        
            if (Spline.Orbit) // for oribiting the spline
            {
                Vector3 Center = GetPoint(Spline.Points[0], Spline.Points[1], Spline.Points[2], Spline.Points[3], T);
                Vector3 TangentVector = GetDirection(T, Spline, Source.transform);
                Vector3 Binormal = GetBiNormal(TangentVector);
                Vector3 NewPoint = GetOrbitPoint(Center, TangentVector, Binormal, Spline, T);
                ObjectToMove.transform.position = NewPoint;
            }

            if (Spline.OscillateH) // horizontal Oscillation
            {
                Vector3 Center = GetPoint(Spline.Points[0], Spline.Points[1], Spline.Points[2], Spline.Points[3], T);
                Vector3 TangentVector = GetDirection(T, Spline, Source.transform);
                Vector3 Binormal = GetBiNormal(TangentVector);
                Vector3 NewPoint = OscillateH(Center, Binormal, Spline.OscillationRangeH, Spline, T);
                ObjectToMove.transform.position = NewPoint;
            }

            if (Spline.OscillateV) // Vertical Oscillation
            {
                Vector3 Center = GetPoint(Spline.Points[0], Spline.Points[1], Spline.Points[2], Spline.Points[3], T);
                Vector3 TangentVector = GetDirection(T, Spline, Source.transform);
                Vector3 Binormal = GetBiNormal(TangentVector);
                Vector3 Normal = GetNormal(TangentVector, Binormal);
                Vector3 NewPoint = OscillateV(Center, Normal, Spline.OscillationRangeV, Spline, T);
                ObjectToMove.transform.position = NewPoint;
            }

            if (Spline.FollowSpline) // follows the Spline Exactly
            {
                Vector3 NewPoint = GetPoint(Spline.Points[0], Spline.Points[1], Spline.Points[2], Spline.Points[3], T);
                ObjectToMove.transform.position = NewPoint;
            }

            UpdateSpline(Spline, Source, Target);

        }
    ```

??? Example "Moving an object"

    ```csharp
        // moves an object along a spline
        public IEnumerator<float> MoveObject( float duration)
        {
            float startTime = Time.time;
    
            float Distance1 = Spline.SplineLength / duration;
            float Distance2 = Vector3.Distance(gameObject.transform.position, Spline.Points[3]);
    
            while (Time.time < startTime + (duration * Spline.SplineScale))
            {
                Distance2 = Vector3.Distance(gameObject.transform.position, Spline.Points[3]);
                float DistanceFraction = Distance2 / Distance1;
                T = Mathf.Lerp(0, 1, (Time.time - startTime) / (duration * Spline.SplineScale));
                SplineMaker2.TraverseSpline(Spline.Caster, Spline.Victim, Spline, Mover, T);
                yield return 0f;
            }
            Destroy(Mover);
            AttackChecklist.Callback();
        }
    ```