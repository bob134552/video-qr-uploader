/*
* Copyright (c) 2014, The WebRTC project authors. All rights reserved.
*
* Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
*
* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
*
* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
*
* Neither the name of Google nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
*
* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
* THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, 
* INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
* OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
*(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

// This code is adapted from
// https://rawgit.com/Miguelao/demos/master/mediarecorder.html

"use strict";

/* globals MediaRecorder */

let mediaRecorder;
let recordedBlobs;

const codecPreferences = 'video/webm;codecs=h264,opus'

const errorMsgElement = document.querySelector("span#errorMsg");
const recordedVideo = document.querySelector("video#recorded");
const recordButton = document.querySelector("button#record");
const gumVideo = document.querySelector("video#gum");
const fileInputElement = $('.file_input');

/* Starts recording and ends recording after 30s */
recordButton.addEventListener("click", () => {
    if (recordButton.textContent === "Start Recording") {
    startRecording();
    setTimeout(function(){ 
        stopRecording();
        recordButton.textContent = "Start Recording";
        playButton.disabled = false;
        downloadButton.disabled = false;
    }, 30000);
    } else {
        stopRecording();
        recordButton.textContent = "Start Recording";
        playButton.disabled = false;
        downloadButton.disabled = false;
    }
});

const playButton = document.querySelector("button#play");
/* Displays recorded video for user */
playButton.addEventListener("click", () => {
    const mimeType = "codecs=h264,opus";
    const superBuffer = new Blob(recordedBlobs, { type: mimeType });
    gumVideo.parentElement.style.display = 'none';
    recordedVideo.parentElement.style.display = 'block';
    recordedVideo.src = null;
    recordedVideo.srcObject = null;
    recordedVideo.src = window.URL.createObjectURL(superBuffer);
    recordedVideo.controls = true;
    recordedVideo.play();
});

const downloadButton = document.querySelector('button#download');
/* Download on click */
downloadButton.addEventListener('click', () => {
    const blob = new Blob(recordedBlobs, {type: 'video/webm'});
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    const order_number = downloadButton.dataset.order_number;
    a.style.display = 'none';
    a.href = url;
    a.download = `video-${order_number}.webm`;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => {
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }, 100);
});

function handleDataAvailable(event) {
    console.log("handleDataAvailable", event);
    if (event.data && event.data.size > 0) {
        recordedBlobs.push(event.data);
    }
}

/* Start Recording */
function startRecording() {
    gumVideo.parentElement.style.display = 'block'
    recordedBlobs = [];
    const mimeType = 'video/webm;codecs=h264,opus'
    const options = { mimeType,
        audioBitsPerSecond: 128000,
        audioConstantBitRate: true,
    };

    try {
        mediaRecorder = new MediaRecorder(window.stream, options);
    } catch (e) {
        console.error("Exception while creating MediaRecorder:", e);
        errorMsgElement.innerHTML = `Exception while creating MediaRecorder: ${JSON.stringify(
        e
        )}`;
        return;
    }

    console.log("Created MediaRecorder", mediaRecorder, "with options", options);
    recordedVideo.parentElement.style.display = 'none'
    recordButton.textContent = "Stop Recording";
    playButton.disabled = true;
    mediaRecorder.onstop = (event) => {
        console.log("Recorder stopped: ", event);
        console.log("Recorded Blobs: ", recordedBlobs);
    };
    mediaRecorder.ondataavailable = handleDataAvailable;
    mediaRecorder.start();
    console.log("MediaRecorder started", mediaRecorder);
}

function stopRecording() {
    mediaRecorder.stop();
}

function handleSuccess(stream) {
    recordButton.disabled = false;
    console.log("getUserMedia() got stream:", stream);
    window.stream = stream;
    gumVideo.srcObject = stream;
}

/* Initialise webcam recorder */
async function init(constraints) {
    try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        handleSuccess(stream);
    } catch (e) {
        console.error("navigator.getUserMedia error:", e);
        errorMsgElement.innerHTML = `navigator.getUserMedia error:${e.toString()}`;
    }
}

/* Creates webcam video */
document.querySelector("button#start").addEventListener("click", async () => {
    gumVideo.parentElement.style.display = 'block';
    document.querySelector("button#start").disabled = true;
    document.querySelector("button#start").style.display = 'none';
    const constraints = {
        audio: {
            echoCancellation: {exact: false}
        },
        video: {
        width: 1280,
        height: 720,
        },
    };
    console.log("Using media constraints:", constraints);
    await init(constraints);
});


$(".upload-form").on('submit', function() {
    $(".spinner-loader").toggleClass('d-none');
    $(".btn-upload-form").attr('disabled', 'disabled');
});