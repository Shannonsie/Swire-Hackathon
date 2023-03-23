var video = document.querySelector("#video");
var startRecord = document.querySelector("#startRecord");
var stopRecord = document.querySelector("#stopRecord");
var downloadLink = document.querySelector("#downloadLink");

        window.onload = async function(){
            stopRecord.style.display = "none";

            videoStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
            video.srcObject = videoStream;
        }

        startRecord.onclick = function(){
            startRecord.style.display = "none";
            stopRecord.style.display = "inline";

            mediaRecorder = new MediaRecorder(videoStream);

            let blob = [];
            mediaRecorder.addEventListener('dataavailable', function(e){
            blob.push(e.data);
            })

            mediaRecorder.addEventListener('stop', function(){
            var videoLocal = URL.createObjectURL(new Blob (blob));
            downloadLink.href = videoLocal;
            })

            mediaRecorder.start();
        }

        stopRecord.onclick = function(){
            mediaRecorder.stop();
        }

// window.onload = function () {
//     navigator.mediaDevices.getUserMedia({audio: true, video: true}).then(stream => {
//         document.getElementById("video").srcObject = stream;
//         document.getElementById("btn").onclick = function (){
//             mediaRecorder = new MediaRecorder(stream);

//             mediaRecorder.start(1000);

//             mediaRecorder.ondataavailable = function(e) {
//                 parts.push(e.data);
//             }
//         }
//     });

//     document.getElementById("stopbtn").onclick = function () {
//         mediaRecorder.stop();
//         const blob = new Blob(parts, {
//             type: "video/webm"
//         });
//         const url = URL.createObjectURL(blob);
//         const a = document.createElement("a");
//         document.body.appendChild(a);
//         a.style = "display: none";
//         a.href = url;
//         a.download = "test.webm";
//         a.click();
//     }
// }