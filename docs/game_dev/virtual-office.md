# Virtual Office / Zoom Background Maker

- A Fun project to generate custom Zoom video, check it out [here](https://github.com/cloudymax/Unity-References/tree/main/ZoomBackgroundMaker).

<figure markdown> <!--  -->
    <video playsinline autoplay muted src="https://thumbs.gfycat.com/SardonicGlaringHorsemouse-mobile.mp4">
    </video>
  <figcaption>Setting up a scene</figcaption>
</figure>

## Features

- 3d environement w/ colliders and physics ready

- Camera control system to get the perfect shot

- Realtime GI, HDRP lighting setup w/ light and reflection probes

- UI system for controlling the post processing and scene lights

- fun video texture integrations and mood items like bloom and flicker

<figure markdown> <!--  -->
    <video playsinline autoplay muted src="https://thumbs.gfycat.com/HorribleUnderstatedIbizanhound-mobile.mp4">
    </video>
  <figcaption>Physics and Lighting tests</figcaption>
</figure>

<figure markdown> <!--  -->
    <video playsinline autoplay muted src="https://thumbs.gfycat.com/BrokenDeadJoey-mobile.mp4">
    </video>
  <figcaption>Halloween at STRIVR</figcaption>
</figure>

# Disclaimers

???+ Warning 

    WiP

    Relies on Enlighten which Unity is dericating and as of the last update has not published a new solution. That was over a year ago - still no update other than it wont be removed form the engine until 2024. I'm guessing their 1.5 Billion dollar acquisition of Weta is supposed to cover this.

    IMO if you want realtime GI in production, grab a VXGI solution like NVIDIA's or SonicEthers- then just run the game at a low res and rely on the new amd upsampeling. Unity's support on RGI is just non-existent.

??? Bug

    - Video textures do not load properly if changed after the initial start().
    - Enlighten is a mess and can break anytime. It works now, but thats as much as anyone can say.