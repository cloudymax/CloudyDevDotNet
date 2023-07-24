let videoSource = new Array();
// swarm ai test
videoSource[0] = 'https://static.videezy.com/system/resources/previews/000/054/376/original/Line_Plexus_Abstract_Network.mp4';
// Landscape Road
// videoSource[1] = 'https://thumbs.gfycat.com/SereneAcceptableAyeaye-mobile.mp4';
// UE4 temple
// videoSource[2] = 'https://thumbs.gfycat.com/AgileOldBuck-mobile.mp4';
// Turret ai
// videoSource[3] = 'https://thumbs.gfycat.com/InbornInnocentCockerspaniel-mobile.mp4';
// grassy sun sweep
// videoSource[4] = 'https://thumbs.gfycat.com/RemarkableGloomyHedgehog-mobile.mp4';
// old pots and rupees
// videoSource[5] = 'https://thumbs.gfycat.com/IllDirectAustraliansilkyterrier-mobile.mp4';
// Justice from above
// videoSource[6] = 'https://thumbs.gfycat.com/FemaleFaithfulBorderterrier-mobile.mp4';
// VR office
// videoSource[7] = 'https://thumbs.gfycat.com/EveryIllinformedCrocodileskink-mobile.mp4';

let i = 0; // global
const videoCount = videoSource.length;
const element = document.getElementById("video-bg");

function videoPlay(videoNum) {
    element.setAttribute("src", videoSource[videoNum]);
    element.autoplay = true;
    element.load();
}
document.getElementById('video-bg').addEventListener('ended', myHandler, false);

videoPlay(0); // load the first video
ensureVideoPlays();	// play the video automatically

function myHandler() {
    i++;
    if (i == videoCount) {
        i = 0;
        videoPlay(i);
    } else {
        videoPlay(i);
    }
}

function ensureVideoPlays() {
    const video = document.getElementById('video-bg');

    if(!video) return;
    
    const promise = video.play();
    if(promise !== undefined){
        promise.then(() => {
            // Autoplay started
        }).catch(error => {
            // Autoplay was prevented.
            video.muted = true;
            video.play();
        });
    }
}
